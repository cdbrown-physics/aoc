use std::{fs, path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result};
use clap::Parser;
use log::{debug, info};
use env_logger;
use regex::Regex;

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}

fn read_lines(filename: &Path)-> Result<(Vec<String>, Vec<u32>)> {
    let file = File::open(filename).context("Failed to open the file")?;

    let reader = BufReader::new(file);
    let mut range_lines: Vec<String> = Vec::new();
    let mut ingredient_id_num: Vec<u32> = Vec::new();
    let mut ingredient_parse: bool = false;
    for line in reader.lines()
    {
        let line_value: String = line?;
        if line_value == "\n" {
            ingredient_parse = true;
            continue;
        }
        if !ingredient_parse {
            range_lines.push(line_value);
        }
        else {
             ingredient_id_num.push(line_value.trim().parse::<u32>()?)
        }
        
    }
    Ok((range_lines, ingredient_id_num))
}

fn part_one(lines: &Vec<String>) -> Result<i32>
{
    Ok(0)
}

fn part_two(lines: &Vec<String>) -> Result<i32>
{
    Ok(0)
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let lines = read_lines(&args.path)?;
    debug!("lines\n\n{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
