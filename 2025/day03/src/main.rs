use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

use anyhow::{Context, Result};
use log::{debug, info};
use env_logger;
use regex::Regex;

fn read_lines(filename: &str) -> Result<Vec<String>>
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

fn get_tens_num_index(line: &String) -> Result<usize> {
    let mut max_tens_int: u32 = 0;
    let mut max_tens_index: usize = 0;
    // Want to return the index of the value that corresponds to the character of the string.
    for i in 0..line.len()-1 {
        let c = line.as_bytes()[i] as char;
        let possible_tens = c.to_digit(10).context("Failed to convert to digit")?;
        if possible_tens > max_tens_int { 
            max_tens_int = possible_tens;
            max_tens_index = i;
        }
    }
    Ok(max_tens_index)
}

fn get_ones_num_index(line: &String, tens_index: usize) -> Result<usize> {
    let mut max_ones_int: u32 = 0;
    let mut max_ones_index: usize = 0;
    // Want to return the index of the value that corresponds to the character of the string.
    for i in (tens_index+1)..line.len() {
        let c = line.as_bytes()[i] as char;
        let possible_ones = c.to_digit(10).context("Failed to convert to digit")?;
        if possible_ones > max_ones_int { 
            max_ones_int = possible_ones;
            max_ones_index = i;
        }
    }
    Ok(max_ones_index)
}

fn find_joltage(line: &String) -> Result<String> {
    let tens_num_index: usize = get_tens_num_index(&line).context("Failed to find tens place number")?;
    let ones_num_index: usize = get_ones_num_index(&line, tens_num_index).context("Failed to find tens place number")?;
    debug!("Indexes found tens: {tens_num_index} ones index: {ones_num_index}");
    let tens_char: char = line.as_bytes()[tens_num_index] as char;
    let ones_char = line.as_bytes()[ones_num_index] as char;
    let joltage = format!("{tens_char}{ones_char}");
    debug!("Number used is {joltage}");
    Ok(joltage)
}

fn part_one(lines: &Vec<String>) -> Result<u32>
{
    let mut total_joltage = 0;
    for line in lines {
        debug!("Looking at line: {line}");
        let joltage = find_joltage(&line)?;
        let num_joltage: u32 = joltage.parse::<u32>()?;
        total_joltage += num_joltage;
    }
    Ok(total_joltage)
}

fn part_two(lines: &Vec<String>) -> Result<i32>
{
    Ok(0)
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let lines = read_lines("data.txt")?;
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
