use std::fs;
use std::io;

use anyhow::{Context, Result};
use log::{debug, info};
use env_logger;
use regex::Regex;

fn read_lines(filename: &str) -> Result<Vec<String>>
{
    let data: String = fs::read_to_string(filename)?;
    let data_iter = data.split(',').map(|s| s.trim().to_string());
    let ranges: Vec<String> = data_iter.collect();
    
    Ok(ranges)
}

fn split_entry(entry: &String) -> Result<(u32, u32)>{
    let range_values: Vec<String> = entry.split('-').map(|s| s.trim().to_string()).collect();
    let start_range: u32 = range_values[0].parse::<u32>()?;
    let end_range: u32 = range_values[1].parse::<u32>()?;

    Ok((start_range, end_range))
}
fn check_repeet(num: u32) -> Result<bool>{
    
}
fn find_invalid_ids(start_range: u32, end_range: u32) -> Result<Vec<u32>> {

    let invalid_ids: Vec<u32> = Vec::new();
    for i in start_range..=end_range
    {
        check_repeet(i);
    }
    Ok(invalid_ids)
}

fn part_one(data: &Vec<String>) -> Result<i32>
{
    for entry in data
    {
        // Again, need to split this range data, this time by the `-`
        let (start_range, end_range) = split_entry(entry)?;
        let invalid_ids = find_invalid_ids(start_range, end_range)?;
    }
    Ok(0)
}

fn part_two(data: &Vec<String>) -> Result<i32>
{
    Ok(0)
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let data = read_lines("data.txt").expect("Failed to read file.");
    debug!("Read in data: {:?}", data);
    let part_one_answer = part_one(&data)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&data)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
