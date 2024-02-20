use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;
use std::str;

pub fn start_docker_containers(version: &String) -> Result<(), String> {
    let home_dir = dirs::home_dir().ok_or("Could not find the home directory.")?;
    let rubra_dir = home_dir.join(".rubra");

    let status = Command::new("docker-compose")
        .args(["pull"])
        .current_dir(&rubra_dir)
        .env("RUBRA_TAG", &version)
        .status()
        .expect("Failed to execute docker-compose");

    if !status.success() {
        return Err("Failed to pull Docker images".to_string());
    }

    let status = Command::new("docker-compose")
        .args(["up", "-d"])
        .current_dir(&rubra_dir)
        .env("RUBRA_TAG", &version)
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
        let stderr = str::from_utf8(&output.stderr).unwrap_or("").trim();

        // Check if the stderr contains specific error text
        if stderr.contains("Cannot connect to the Docker daemon") {
            return Err("Docker stopped".to_string());
        }

        // For other errors, you can return or handle them as needed
        return Err("No Rubra containers are running".to_string());
    }

    let stdout = str::from_utf8(&output.stdout).unwrap_or("").trim();
    // Split the stdout by whitespace and create a vector of tuples
    // Assuming each container name is followed by a status or similar property, adjust accordingly
    let containers = stdout
        .split_whitespace()
        .map(|name| (name.to_string(), "Unknown Status".to_string())) // Placeholder for actual status
        .collect::<Vec<(String, String)>>();

    Ok(containers)
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
