use std::fs;
use std::io;

use anyhow::{Context, Result};
use log::{debug, info};
use env_logger;


fn read_lines(filename: &str) -> Result<Vec<String>>
{
    let data: String = fs::read_to_string(filename)?;
    let data_iter = data.split(',').map(|s| s.trim().to_string());
    let ranges: Vec<String> = data_iter.collect();
    
    Ok(ranges)
}

fn split_entry(entry: &String) -> Result<(u64, u64)>{
    let range_values: Vec<String> = entry.split('-').map(|s| s.trim().to_string()).collect();
    let start_range: u64 = range_values[0].parse::<u64>()?;
    let end_range: u64 = range_values[1].parse::<u64>()?;

    Ok((start_range, end_range))
}
fn id_repeet(num: u64) -> bool{
    let str_number: String = num.to_string();
    let mid_val = str_number.len() / 2;
    let first_half = &str_number[..mid_val];
    let second_half = &str_number[mid_val..];
    if first_half == second_half
    {
        return true
    }
    else
    {
        // println!("{first_half} ands {second_half} don't match");
        return false
    }
    
}
fn find_invalid_ids(start_range: u64, end_range: u64) -> Result<Vec<u64>> {

    // println!("Checking range of {start_range} to {end_range}");
    let mut invalid_ids: Vec<u64> = Vec::new();
    for i in start_range..=end_range
    {
        // println!("Checking {i}");
        if id_repeet(i)
        {
            // println!("Id: {i} is a repeet.");
            invalid_ids.push(i);
        }
    }
    Ok(invalid_ids)
}

fn part_one(data: &Vec<String>) -> Result<u64>
{
    let mut answer: u64 = 0;
    for entry in data
    {
        // Again, need to split this range data, this time by the `-`
        let (start_range, end_range) = split_entry(entry)?;
        let invalid_ids = find_invalid_ids(start_range, end_range)?;
        // println!{"Found the invalids {:?}", invalid_ids};
        let s: u64 = invalid_ids.iter().sum();
        answer += s;
    }
    Ok(answer)
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
