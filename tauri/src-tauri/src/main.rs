// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod compose;

use compose::*;
use dirs;
use reqwest;
use std::env;
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;
use std::sync::{Arc, Mutex};
use tauri::Manager;
use tauri::Window;
use tauri::{
    CustomMenuItem, SystemTray, SystemTrayEvent, SystemTrayMenu, WindowBuilder, WindowUrl,
};
use tokio_stream::StreamExt;

struct RubraState {
    rubra_dir: PathBuf,
    llm_file: PathBuf,
    llm_process: Option<std::process::Child>,
    app_version: String,
}

#[cfg(target_os = "windows")]
const DEFAULT_DOCKER_PATH: &str = "C:\\Program Files\\Docker\\Docker\\resources\\bin";
#[cfg(target_os = "macos")]
const DEFAULT_DOCKER_PATH: &str = "/usr/local/bin:/usr/bin";

#[cfg(target_os = "windows")]
const MODEL_FILE_URL: &str =
    "https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/llamafile.exe";
#[cfg(target_os = "macos")]
const MODEL_FILE_URL: &str =
    "https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/rubra.llamafile";

#[cfg(target_os = "windows")]
const MODEL_FILE_GGUF_URL: &str = "https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf";

fn add_docker_paths_to_app() -> Result<String, String> {
    let mut path = env::var("PATH").map_err(|_| "".to_string())?;
    let home_dir = dirs::home_dir().ok_or("Could not find the home directory.")?;

    #[cfg(any(target_os = "windows", target_os = "macos"))]
    {
        path.push_str(if cfg!(target_os = "windows") {
            ";"
        } else {
            ":"
        });
        path.push_str(DEFAULT_DOCKER_PATH);
        if cfg!(target_os = "macos") {
            path.push_str(":");
            path.push_str(&home_dir.join(".rd").join("bin").to_string_lossy());
        }
    }
    env::set_var("PATH", &path);
    Ok(path)
}

#[tauri::command]
fn check_docker_and_compose() -> Result<(String, String), String> {
    let path = add_docker_paths_to_app()?;
    let docker_check = Command::new("docker").arg("--version").output();

    let compose_check = Command::new("docker-compose").arg("--version").output();

    match (docker_check, compose_check) {
        (Ok(docker_output), Ok(compose_output)) => {
            if docker_output.status.success() && compose_output.status.success() {
                let docker_version = String::from_utf8_lossy(&docker_output.stdout).to_string();
                let compose_version = String::from_utf8_lossy(&compose_output.stdout).to_string();
                Ok((docker_version, compose_version))
            } else {
                Err("Docker or Docker Compose is not installed".to_string())
            }
        }
        _ => Err(format!(
            "Failed to execute docker or docker-compose commands in PATH: {}",
            path
        )),
    }
}

fn create_and_initialize_rubra_dir(base_dir: &PathBuf, app: &tauri::App) -> Result<(), String> {
    let rubra_dir = base_dir.join(".rubra");
    let compose_resource_path = app
        .handle()
        .path_resolver()
        .resolve_resource("assets/docker-compose.yml")
        .expect("could not resolve resource 'docker-compose.yml'");

    if !rubra_dir.exists() {
        fs::create_dir_all(&rubra_dir)
            .map_err(|_| format!("Failed to create directory at {:?}", rubra_dir))?;
    }

    if let Ok(metadata) = rubra_dir.metadata() {
        if !metadata.permissions().readonly() {
            let _ = populate_etcd_yaml_file(&rubra_dir)?;
            let _ = write_llm_config(&rubra_dir)?;
            let _ = write_compose_yaml(&rubra_dir, &compose_resource_path)?;
            return Ok(());
        }
    }

    let _result = OpenOptions::new()
        .write(true)
        .open(&rubra_dir)
        .map_err(|_| format!("Failed to set write permissions on {:?}", rubra_dir))?;

    let _ = populate_etcd_yaml_file(&rubra_dir)?;
    let _ = write_llm_config(&rubra_dir)?;
    let _ = write_compose_yaml(&rubra_dir, &compose_resource_path)?;

    Ok(())
}

fn write_llm_config(rubra_dir: &PathBuf) -> Result<(), String> {
    let yaml_file_path = rubra_dir.join("llm-config.yaml");

    if !yaml_file_path.exists() {
        let mut file =
            File::create(&yaml_file_path).map_err(|e| format!("Failed to create file: {:?}", e))?;

        let contents = "\
model_list:
  # Local Model
  - model_name: custom
    litellm_params:
      model: openai/custom
      api_base: \"http://host.docker.internal:1234/v1\"
      api_key: \"None\"
      custom_llm_provider: \"openai\"

  # OpenAI GPT-4
  # - model_name: gpt-4-1106-preview
  #   litellm_params:
  #     model: gpt-4-1106-preview
  #     api_key: \"OPENAI_API_KEY\"
  #     custom_llm_provider: \"openai\"

  # Anthropic Claude
  # - model_name: claude-2.1
  #   litellm_params:
  #     model: claude-2.1
  #     api_key: \"ANTHROPIC_API_KEY\"

litellm_settings:
  drop_params: True
  set_verbose: True
  cache: True

environment_variables:
  REDIS_HOST: \"redis\"
  REDIS_PORT: \"6379\"
  REDIS_PASSWORD: \"\"";

        file.write_all(contents.as_bytes())
            .map_err(|e| format!("Failed to write to file: {:?}", e))?;
    }

    Ok(())
}

fn populate_etcd_yaml_file(rubra_dir: &PathBuf) -> Result<(), String> {
    let yaml_file_path = rubra_dir.join("embedEtcd.yaml");
    if !yaml_file_path.exists() {
        let mut file =
            File::create(&yaml_file_path).map_err(|e| format!("Failed to create file: {:?}", e))?;

        let contents = "\
listen-client-urls: http://0.0.0.0:2379
advertise-client-urls: http://0.0.0.0:2379";

        file.write_all(contents.as_bytes())
            .map_err(|e| format!("Failed to write to file: {:?}", e))?;
    }

    Ok(())
}

#[tauri::command]
async fn download_rubra_llamafile(
    window: Window,
    state: tauri::State<'_, Arc<Mutex<RubraState>>>,
) -> Result<String, String> {
    let rubra_llamafile_url = MODEL_FILE_URL.to_string();
    let rubra_llamafile_path = state.lock().unwrap().llm_file.clone();

    if !rubra_llamafile_path.exists() {
        let response = reqwest::get(rubra_llamafile_url)
            .await
            .map_err(|e| e.to_string())?;

        let total_size = response
            .content_length()
            .ok_or("Failed to get content length")?;

        let mut stream = response.bytes_stream();

        let mut downloaded: u64 = 0;
        let mut file = File::create(rubra_llamafile_path.clone()).map_err(|e| e.to_string())?;

        while let Some(item) = stream.next().await {
            let chunk = item.map_err(|e| e.to_string())?;
            file.write_all(&chunk).map_err(|e| e.to_string())?;
            downloaded += chunk.len() as u64;

            let progress = downloaded as f64 / total_size as f64;
            window.emit("download-progress", progress).unwrap();
        }
    }

    #[cfg(target_os = "windows")]
    {
        // Download the additional .gguf file for Windows
        let gguf_file_path = rubra_dir.join("openhermes.gguf");
        if !gguf_file_path.exists() {
            let gguf_url = MODEL_FILE_GGUF_URL.to_string();
            download_file(&gguf_url, &gguf_file_path, &window).await?;
        }
    }

    // Setting executable permissions
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut perms = fs::metadata(&rubra_llamafile_path)
            .map_err(|e| format!("Failed to read metadata: {}", e))?
            .permissions();
        perms.set_mode(0o755); // Read, write, and execute for owner, read and execute for others
        fs::set_permissions(&rubra_llamafile_path, perms)
            .map_err(|e| format!("Failed to set permissions: {}", e))?;
    }

    window
        .emit(
            "download-complete",
            rubra_llamafile_path.to_string_lossy().to_string(),
        )
        .unwrap();

    Ok("rubra.llamafile is ready".to_string())
}

#[cfg(target_os = "windows")]
async fn download_file(url: &str, file_path: &PathBuf, window: &Window) -> Result<(), String> {
    let response = reqwest::get(url).await.map_err(|e| e.to_string())?;
    let total_size = response
        .content_length()
        .ok_or("Failed to get content length")?;

    let mut stream = response.bytes_stream();
    let mut file = File::create(file_path.clone()).map_err(|e| e.to_string())?;
    let mut downloaded: u64 = 0;

    while let Some(item) = stream.next().await {
        let chunk = item.map_err(|e| e.to_string())?;
        file.write_all(&chunk).map_err(|e| e.to_string())?;
        downloaded += chunk.len() as u64;

        let progress = downloaded as f64 / total_size as f64;
        window.emit("download-progress", progress).unwrap();
    }

    Ok(())
}

#[tauri::command]
fn execute_rubra_llamafile(
    state: tauri::State<'_, Arc<Mutex<RubraState>>>,
) -> Result<String, String> {
    let mut state = state.lock().unwrap();

    if state.llm_process.is_some() {
        return Ok("rubra.llamafile is already running".to_string());
    }
    if state.llm_file.exists() {
        let child = Command::new(state.llm_file.to_string_lossy().to_string())
            .arg("-c")
            .arg("16000")
            .spawn()
            .map_err(|e| format!("Failed to execute rubra.llamafile: {}", e))?;

        state.llm_process = Some(child);

        Ok("rubra.llamafile is started".to_string())
    } else {
        Err("rubra.llamafile does not exist".to_string())
    }
}

fn stop_llm_process(process: &mut std::process::Child) -> Result<String, String> {
    process
        .kill()
        .map_err(|e| format!("Failed to stop process: {}", e))?;
    Ok("Process is stopped".to_string())
}

#[tauri::command]
async fn check_rubra_llamafile_ready() -> Result<String, String> {
    for _ in 0..5 {
        match reqwest::Client::new()
            .post("http://localhost:1234/v1/chat/completions")
            .json(&serde_json::json!({
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "respond with 'pong' when someone sends 'ping'"
                    },
                    {
                        "role": "user",
                        "content": "ping"
                    }
                ]
            }))
            .send()
            .await
        {
            Ok(response) => {
                println!("We got{:?}", response.status());
                if response.status().is_success() {
                    return Ok("Local model is ready and accepting requests.".to_string());
                }
            }
            Err(_) => {
                // Wait for 5 seconds before retrying
                tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
            }
        }
    }

    Err("Rubra's local model is not accepting requests.".to_string())
}

#[tauri::command]
async fn rubra_event(
    event: &str,
    state: tauri::State<'_, Arc<Mutex<RubraState>>>,
) -> Result<Vec<(String, String)>, String> {
    let version = state.lock().unwrap().app_version.clone();
    if event == "start" {
        let _ = start_docker_containers(&version);
        let _ = execute_rubra_llamafile(state);
    } else if event == "stop" {
        let mut state_lock = state.lock().unwrap();
        if let Some(process) = &mut state_lock.llm_process {
            let _ = stop_llm_process(process);
            state_lock.llm_process = None;
        }

        let _ = stop_docker_containers();
    }

    check_containers_status("rubra")
}

#[tauri::command]
async fn check_rubra_container_status() -> Result<Vec<(String, String)>, String> {
    check_containers_status("rubra")
}

fn main() {
    let tray_menu = SystemTrayMenu::new()
        .add_item(CustomMenuItem::new("show", "Go To Rubra System Dashboard"))
        .add_item(CustomMenuItem::new("ui", "Go To Rubra UI"));

    let llamfile_name = if cfg!(target_os = "windows") {
        "llamafile.exe"
    } else {
        "rubra.llamafile"
    };

    let state = Arc::new(Mutex::new(RubraState {
        rubra_dir: dirs::home_dir().unwrap().join(".rubra"),
        llm_file: dirs::home_dir().unwrap().join(".rubra").join(llamfile_name),
        llm_process: None,
        app_version: "".to_string(),
    }));

    tauri::Builder::default()
        .system_tray(SystemTray::new().with_menu(tray_menu))
        .manage(state.clone())
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::MenuItemClick { id, .. } => match id.as_str() {
                "show" => {
                    if let Some(window) = app.get_window("main") {
                        // If the window exists, show and focus
                        window.show().unwrap();
                        window.set_focus().unwrap();
                    } else {
                        // If the window does not exist, create a new one
                        let _new_window =
                            WindowBuilder::new(app, "main", WindowUrl::App("index.html".into()))
                                .title("My App")
                                .build()
                                .expect("Failed to create window");
                    }
                }
                "ui" => {
                    let window = app.get_window("main").unwrap();
                    tauri::api::shell::open(&window.shell_scope(), "http://localhost:8501", None)
                        .unwrap();
                }
                _ => {}
            },
            _ => {}
        })
        .setup(move |app| {
            let home_dir = dirs::home_dir().ok_or("Could not find the home directory.")?;
            match create_and_initialize_rubra_dir(&home_dir, &app) {
                Ok(_) => {
                    println!("Rubra directory is ready");
                }
                Err(e) => eprintln!("Error: {}", e),
            }
            let app_version = format!("v{}", app.package_info().version.to_string());
            state.lock().unwrap().app_version = app_version.clone();
            state.lock().unwrap().rubra_dir = home_dir.join(".rubra");

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            check_docker_and_compose,
            download_rubra_llamafile,
            execute_rubra_llamafile,
            check_rubra_llamafile_ready,
            check_rubra_container_status,
            rubra_event,
        ])
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|_app_handle, event| match event {
            tauri::RunEvent::ExitRequested { api, .. } => {
                api.prevent_exit();
            }
            tauri::RunEvent::Exit => {
                let app_handle_clone = _app_handle.clone();
                let rubra_state_arc = app_handle_clone.state::<Arc<Mutex<RubraState>>>();

                let _ = stop_docker_containers();

                let mut rubra_state = rubra_state_arc.lock().unwrap();
                if let Some(child) = &mut rubra_state.llm_process {
                    let _ = stop_llm_process(child);
                    rubra_state.llm_process = None;
                }
            }
            _ => {}
        })
}
