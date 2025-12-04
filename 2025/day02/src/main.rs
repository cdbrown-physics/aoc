use std::fs;

use anyhow::{Result};
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

fn id_repeat(num: u64) -> bool{
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
        debug!("{first_half} ands {second_half} don't match");
        return false
    }
    
}

fn find_invalid_ids(start_range: u64, end_range: u64) -> Result<Vec<u64>> {

    debug!("Checking range of {start_range} to {end_range}");
    let mut invalid_ids: Vec<u64> = Vec::new();
    for i in start_range..=end_range
    {
        // println!("Checking {i}");
        if id_repeat(i)
        {
            // println!("Id: {i} is a repeat.");
            invalid_ids.push(i);
        }
    }
    Ok(invalid_ids)
}

fn splice_str_num(str_num: &String, splice_len: usize) -> Result<Vec<String>>{
    let mut spliced_vec_str: Vec<String> = Vec::new();
    let mut char_index: usize = 0;
    let mut next_index = splice_len;
    loop {
        /* Need to add .to_string at the end of this line because indexing is a problem without it. Rust is worried 
        that str_num might not be asc-ii characters. And if that's the case, then doing the indexing might end up in 
        the middle of a char and cause problems. the to_string seems to fix that worry */ 
        let tmp_str: String = str_num[char_index..next_index].to_string(); 
        debug!("Temp string is {tmp_str}");
        spliced_vec_str.push(tmp_str);
        char_index = next_index;
        next_index += splice_len;
        if next_index >= str_num.len(){
            // Next loop will take us out of bounds. So take whatever is left and add it
            spliced_vec_str.push(str_num[char_index..].to_string());
            break
        }
    }
    debug!("Spliced vector is now: {:?}", spliced_vec_str);
    Ok(spliced_vec_str)
}

fn any_id_repeat(num: u64) -> bool{
    debug!("Checking number {num}");
    let str_number = num.to_string();
    let mid_val = str_number.len() / 2;
    for i in 1..=mid_val{
        debug!("Checking splice range of {i}");
        let spliced_vec_numbers: Vec<String> = match splice_str_num(&str_number, i){
            Ok(vector) => vector,
            Err(e) => { eprint!("Error parsing number string: {:?}", e); return false; }
        };
        let first_element = &spliced_vec_numbers[0];
        if spliced_vec_numbers.iter().all(|e| e == first_element){
            // All the elements match, this is a problem id
            return true
        }
    }
    // Iterated through all possible splits of the number, and none of them were repeats so must be ok
    false
}

fn find_any_invalid_ids(start_range: u64, end_range: u64) -> Result<Vec<u64>> {
    let mut invalid_ids: Vec<u64> = Vec::new();
    debug!("Checking id ranges {start_range}, {end_range}");
    for i in start_range..=end_range {
        if any_id_repeat(i){
            invalid_ids.push(i)
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

fn part_two(data: &Vec<String>) -> Result<u64>
{
    let mut answer: u64 = 0;
    for entry in data {
        // Again, need to split this range data, this time by the `-`
        let (start_range, end_range) = split_entry(entry)?;
        let invalid_ids = find_any_invalid_ids(start_range, end_range)?;
        // println!{"Found the invalids {:?}", invalid_ids};
        let s: u64 = invalid_ids.iter().sum();
        answer += s;
    }
    Ok(answer)
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
