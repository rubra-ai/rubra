use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

pub fn start_docker_containers() -> Result<(), String> {
    let home_dir = dirs::home_dir().ok_or("Could not find the home directory.")?;
    let rubra_dir = home_dir.join(".rubra");

    let cargo_version = env!("CARGO_PKG_VERSION");
    let version = if cargo_version == "0.0.0" {
        "main".to_string()
    } else {
        format!("v{}", cargo_version)
    };

    let status = Command::new("docker-compose")
        .args(["pull"])
        .current_dir(&rubra_dir)
        .env("RUBRA_TAG", version)
        .status()
        .expect("Failed to execute docker-compose");

    if !status.success() {
        return Err("Failed to pull Docker images".to_string());
    }

    let status = Command::new("docker-compose")
        .args(["up", "-d"])
        .current_dir(&rubra_dir)
        .status()
        .expect("Failed to execute docker-compose");

    if !status.success() {
        return Err("Failed to start Docker containers".to_string());
    }

    Ok(())
}

pub fn stop_docker_containers() -> Result<(), String> {
    let home_dir = dirs::home_dir().ok_or("Could not find the home directory.")?;
    let rubra_dir = home_dir.join(".rubra");

    let status = Command::new("docker-compose")
        .args(["down"])
        .current_dir(&rubra_dir)
        .status()
        .expect("Failed to execute docker-compose");

    if !status.success() {
        return Err("Failed to stop Docker containers".to_string());
    }

    Ok(())
}

pub fn check_containers_status(network: &str) -> Result<Vec<(String, String)>, String> {
    let output = Command::new("docker")
        .args([
            "network",
            "inspect",
            network,
            "-f",
            "{{range .Containers}}{{.Name}} {{end}}",
        ])
        .output()
        .expect("Failed to inspect Docker network");

    if !output.status.success() {
        return Err("Failed to get container IDs".to_string());
    }

    let container_ids = String::from_utf8(output.stdout).unwrap();
    let mut container_statuses = Vec::new();

    for container_id in container_ids.split_whitespace() {
        let output = Command::new("docker")
            .args(["inspect", "--format", "{{.State.Status}}", container_id])
            .output()
            .expect("Failed to inspect container");

        if output.status.success() {
            let status = String::from_utf8(output.stdout).unwrap();
            container_statuses.push((container_id.to_string(), status));
        } else {
            container_statuses.push((container_id.to_string(), "unknown".to_string()));
        }
    }

    Ok(container_statuses)
}

pub fn write_compose_yaml(rubra_dir: &PathBuf, compose_resource: &PathBuf) -> Result<(), String> {
    let compose_file_path = rubra_dir.join("docker-compose.yml");
    let mut output = File::create(&compose_file_path).unwrap();

    let contents = fs::read(&compose_resource)
        .map_err(|e| format!("Failed to read compose resource: {}", e))?;

    output
        .write_all(&contents)
        .map_err(|e| format!("Failed to write compose file: {}", e))?;

    Ok(())
}
