use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result};
use clap::Parser;
use log::{debug, info, warn};

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}
fn read_lines(filename: &Path) -> Result<Vec<String>> {
    let file = File::open(filename).context("Failed to open the file")?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        let line_content = line?;
        lines.push(line_content);
    }
    Ok(lines)
}

fn part_one(lines: &Vec<String>) -> Result<u32>= {
    Ok(0)
}

fn part_two(lines: &Vec<String>) -> Result<u32> {
    Ok(0)
}

fn main() -> Result<()> {
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let mut lines = read_lines(&args.path)?;
    debug!("lines\n\n{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
