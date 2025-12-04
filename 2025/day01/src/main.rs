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

fn get_clicks(line: &str) -> Result<i32>
{
    let re = Regex::new(r"\d+")?;
    let m = re.find(line).context("Failed to find a number in the string.")?;
    let turn_count = m.as_str().parse::<i32>()?;
    Ok(turn_count)
}


fn positive_mod(a: i32, n: i32) -> i32
{
    // Mod that handles `a` being negative or positive.
    let r = a % n;
    (r + n) % n
}
fn turn_dial(dial: i32, turn: i32) -> Result<i32>
{
    // Add the turn amount to the dial
    let mut new_dial: i32 = dial + turn;
    new_dial = positive_mod(new_dial, 100);
    Ok(new_dial)
}

fn turn_dial_count_zero(dial: i32, turn: i32) -> Result<(i32, i32)>
{
    let mut zero_count = 0;

    // How many multiples of 100? 
    let multiple_zeros: i32 = turn.abs() / 100;
    zero_count += multiple_zeros; // Add those zeros on
    let remainder_turn = turn % 100; // Could be positive or negative
    let mut new_dial = dial + remainder_turn;
    if new_dial * dial < 0 // sign change always crossed zero
    {
        zero_count += 1;
    }
    else if new_dial > 100 
    {
        zero_count += 1;
    }
    new_dial = positive_mod(new_dial, 100); // Adjust for rollovers
 
    Ok((zero_count,new_dial))
}

fn part_one(lines: &Vec<String>) -> Result<i32>
{
    let mut zero_count = 0;
    let mut dial_number: i32 = 50; // Dial starting position
    for line in lines
    {
        let turn_direction = line.chars().next().unwrap(); // Get first char string to determine direction of turning
        debug!("{turn_direction}");
        if turn_direction == 'L'
        {
            debug!("Turning left");
            let turn_count = get_clicks(&line)? * -1;
            dial_number = turn_dial(dial_number, turn_count)?;
        }
        else if turn_direction == 'R'
        {
            debug!("Truning right");
            let turn_count = get_clicks(&line)?;
            dial_number = turn_dial(dial_number, turn_count)?;
        }
        debug!("Dial is now at: {dial_number}");
        if dial_number == 0
        {
            zero_count += 1;
        }
    }
    Ok(zero_count)
}

fn part_two(lines: &Vec<String>) -> Result<i32>
{
    let mut holder_temp: (i32, i32) = (0, 50);
    let mut zero_count: i32 = holder_temp.0;
    let mut dial_number: i32 = holder_temp.1; // Dial starting position
    for line in lines
    {
        let turn_direction = line.chars().next().unwrap(); // Get first char string to determine direction of turning
        if turn_direction == 'L'
        {
            let turn_count = get_clicks(&line)? * -1;
            
            holder_temp = turn_dial_count_zero(dial_number, turn_count)?;
            zero_count += holder_temp.0;
            dial_number = holder_temp.1;
            debug!("Turning left {turn_count}. Zero count is at {zero_count}");

        }
        else if turn_direction == 'R'
        {
            let turn_count = get_clicks(&line)?;
            holder_temp = turn_dial_count_zero(dial_number, turn_count)?;
            zero_count += holder_temp.0;
            dial_number = holder_temp.1;
            debug!("Truning right {turn_count}. Zero count is at {zero_count}");
        }
        debug!("Dial is now at: {dial_number}");
        if dial_number == 0
        {
            zero_count += 1;
        }
    }
    Ok(zero_count)
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let lines = read_lines("data.txt").expect("Failed to read file.");
    debug!("{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
