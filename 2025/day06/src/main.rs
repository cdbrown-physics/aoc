use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result, anyhow};
use clap::Parser;
use log::{debug, info};

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}
fn read_lines(filename: &Path) -> Result<Vec<Vec<String>>> {
    let path = Path::new(filename);
    let file = File::open(&path)?;

    let reader = BufReader::new(file);
    let mut lines = Vec::new();

    for line in reader.lines() {
        let line_content: Vec<String> = line?.split_ascii_whitespace().map(|s| s.to_string()).collect();
        debug!("Line contents are {line_content:?}");
        lines.push(line_content);
    }
    Ok(lines)
}

fn sum_numbers(operator_vec: Vec<String>) -> Result<u64> {
    let mut sum = 0;
    debug!("Summing these numbers {operator_vec:?}");
    // loop over vector expect for last element
    for s in operator_vec.iter().take(operator_vec.len() - 1) {
        sum += s.parse::<u64>().context("Cannot turn elemetn into a u64")?;
    }
    debug!("The sum is {sum}");
    Ok(sum)
}

fn prod_numbers(operator_vec: Vec<String>) -> Result<u64> {
    let mut prod = 1;
    debug!("Product of these numbers {operator_vec:?}");
    for s in operator_vec.iter().take(operator_vec.len() - 1) {
        prod *= s.parse::<u64>().context("Cannot turn element into a u64")?;
    }
    debug!("The product is {prod}");
    Ok(prod)
}

fn extra_data_parse(filename: &Path) -> Result<Vec<Vec<char>>> {
    let path = Path::new(filename);
    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut grid: Vec<Vec<char>> = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let char_line: Vec<char> = line.chars().collect();
        grid.push(char_line);
    }
    Ok(grid)
}

fn build_column(char_lines: &Vec<Vec<char>>, i: usize) -> Vec<char> {
    let number_of_lines: usize = char_lines.len();
    let mut column: Vec<char> = Vec::new();
    for n in 0..number_of_lines {
        column.push(char_lines[n][i]);
    }
    column
}

fn get_number(column: Vec<char>) -> Result<u64> {
    /* Take a column of chars and returns a number */
    let s: String = column.iter().collect();
    let num: u64 = s.trim().parse::<u64>()?;
    Ok(num)
}

fn multiply_numbers(numbers: &[u64]) -> u64 {
    debug!("Multiplying numbers {numbers:?}");
    let mut answer = 1;
    for i in numbers {
        answer *= i
    }
    answer
}
fn add_numbers(numbers: &[u64]) -> u64 {
    debug!("Adding numbers {numbers:?}");
    let mut answer = 0;
    for i in numbers {
        answer += i;
    }
    answer
}

fn part_one(lines: &Vec<Vec<String>>) -> Result<u64> {
    let base_vec_len: usize = lines[0].len();
    let number_of_operators: usize = lines.len();
    let mut answer: u64 = 0;
    for i in 0..base_vec_len {
        let mut operator_vec: Vec<String> = Vec::new();
        for n in 0..number_of_operators {
            operator_vec.push(lines[n][i].clone());
        }
        if operator_vec.is_empty() {
            return Err(anyhow!("operator vector is empty"));
        }
        // Now operator_vec is a vector with the numbers, and the operation at the end.
        let operation = operator_vec.last().context("Failed to get last element of vector")?;
        if operation == "+" {
            answer += sum_numbers(operator_vec)?;
        }
        else if operation == "*" {
            answer += prod_numbers(operator_vec)?;
        }
        else {
            return Err(anyhow!("Bad operator passed in {operation}"))
        }
    }
    Ok(answer)
}

fn part_two(char_lines: &Vec<Vec<char>>) -> Result<u64> {
    debug!("Simple charred parse {char_lines:?}");
    let chars_in_line: usize = char_lines[0].len();
    let mut answer: u64 = 0;
    let mut numbers: Vec<u64> = Vec::new();
    for i in (0..chars_in_line).rev() {
        let mut column = build_column(char_lines, i);
        debug!("Looking at column: {column:?}");
        // Check for new sections. We'll know it's a new section if the whole column is empty space.
        if column.iter().all(|c| c.is_whitespace()) {
            debug!("New math operation");
            numbers.clear();
            continue;
        }
        else if column.iter().any(|&c| c == '*') {
            column.pop();
            numbers.push(get_number(column)?);
            answer += multiply_numbers(&numbers);
            debug!("Multiplication")
        }
        else if column.iter().any(|&c| c == '+') {
            column.pop();
            numbers.push(get_number(column)?);
            answer += add_numbers(&numbers);
            debug!("Addtion")
        }
        else {
            numbers.push(get_number(column)?);
        }
    }
    Ok(answer)
}

fn main() -> Result<()> {
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let lines = read_lines(&args.path)?;
    debug!("lines\n\n{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let char_lines = extra_data_parse(&args.path)?;
    let part_two_answer = part_two(&char_lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
