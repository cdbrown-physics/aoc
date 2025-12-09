use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

use anyhow::{Context, Result};
use clap::Parser;
use log::{debug, info};

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}
fn read_lines(filename: &Path) -> Result<Vec<Vec<char>>> {
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


fn part_one(lines: &[Vec<char>]) -> Result<u32> {
    let mut tachyon_beam: Vec<usize> = Vec::new();
    let mut split_count: u32 = 0;
    // Vector will keep track of where the beam is. When we hit a `^` character add it to the left and right of those spots
    let start_index: usize = lines[0].iter().position(|&c| c=='S').context("Failed to find the start tachyon")?;
    debug!("Starting index at: {start_index}");
    tachyon_beam.push(start_index);
    for i in 1..lines.len() {
        let mut new_tachyons: Vec<usize> = Vec::new();
        debug!("Current tachyon beam is at {tachyon_beam:?}");
        for t in &tachyon_beam {
            // Look at line and see if there's a splitter on that spot
            if lines[i][*t] == '^' {
                // Then the beam hit a splitter add tachyon to the left and right of splitter but only if in range
                new_tachyons.extend([t-1, t+1]);
                split_count += 1;
            }
            else {
                // Beam didn't hit anything and need to keep traveling
                new_tachyons.push(*t);
            }
        }
        debug!("New tachyon beam is {new_tachyons:?}");
        debug!("Current count is {split_count}");
        // Replace the tachyon beam with all the new values
        if !new_tachyons.is_empty(){
            new_tachyons.sort_unstable();
            new_tachyons.dedup();
            tachyon_beam = new_tachyons;
        }
    }
    Ok(split_count)
}

fn part_two(lines: &[Vec<char>]) -> Result<usize> {
    let mut tachyon_beam: HashMap<usize, usize> = HashMap::new();
    // Vector will keep track of where the beam is. When we hit a `^` character add it to the left and right of those spots
    let start_index: usize = lines[0].iter().position(|&c| c=='S').context("Failed to find the start tachyon")?;
    debug!("Starting index at: {start_index}");
    tachyon_beam.insert(start_index, 1);
    for i in 1..lines.len() {
        let mut new_tachyons: HashMap<usize, usize> = HashMap::new();
        debug!("Current tachyon beam is at {tachyon_beam:?}");
        for (key, value) in &tachyon_beam {
            // Look at line and see if there's a splitter on that spot
            let key_val = *key;
            if lines[i][key_val] == '^' {
                // Then the beam hit a splitter add tachyon to the left and right of splitter but only if in range
                *new_tachyons.entry(key_val + 1).or_insert(0) += value;
                *new_tachyons.entry(key_val - 1).or_insert(0) += value;
                        }
            else {
                *new_tachyons.entry(key_val).or_insert(0) += value;
            }
        }
        // Replace the tachyon beam with all the new values
        if !new_tachyons.is_empty(){
            tachyon_beam = new_tachyons;
        }
    }
    let mut timeline_count: usize = 0;
    for (_, value) in &tachyon_beam {
        timeline_count += value;
    }
    Ok(timeline_count)
}

fn main() -> Result<()> {
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
