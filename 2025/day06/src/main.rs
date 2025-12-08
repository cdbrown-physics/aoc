use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result, anyhow};
use clap::Parser;
use log::{debug, info, warn};

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
        if (char_line.len() + 1) % 4 != 0 {
            return Err(anyhow!("parsed char line is missing something {char_line:?}"));
        }
        grid.push(char_line);
    }
    Ok(grid)
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
    let base_vec_len: usize = char_lines[0].len();
    let number_of_operators: usize = char_lines.len();
    let mut answer: u64 = 0;
    for i in 0..base_vec_len {
        let mut operator_vector: Vec<String> = Vec::new();
    }
    Ok(0)
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
