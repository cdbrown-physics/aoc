use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

use anyhow::{Context, Result};
use log::{debug, info};
use env_logger;
use regex::Regex;

fn read_lines(filename: &str) -> io::Result<Vec<String>>
{
    let path = Path::new(filename);
    let file = File::open(&path)?;

    let reader = io::BufReader::new(file);
    let mut lines = Vec::new();

    for line in reader.lines()
    {
        let line_content = line?;
        lines.push(line_content);
    }
    Ok(lines)
}

fn part_one(lines: &Vec<String>) -> Result<i32>
{
    Ok()
}

fn part_two(lines: &Vec<String>) -> Result<i32>
{
    Ok()
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
