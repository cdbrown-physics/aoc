use std::{fs, path::{Path, PathBuf}};

use anyhow::{Result};
use clap::Parser;
use log::{debug, info};
use env_logger;

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}

fn read_lines(filename: &Path) -> Result<Vec<Vec<char>>>
{
    let file = fs::read_to_string(filename)?;
    let grid: Vec<Vec<char>> = file.lines().map(|line| line.chars().collect()).collect();
    Ok(grid)
}

fn get_neighbor_count(lines: &Vec<Vec<char>>, y: usize, x: usize) -> u8 {
    let mut neighbor_count = 0;
    let y_bound = lines.len() - 1;
    let x_bound = lines.len() -1;
    // Check the 3 squares above this character
    if y > 0  && x > 0 && lines[y-1][x-1] == '@'                 { neighbor_count += 1; } // Up and Left
    if y > 0  && lines[y-1][x] == '@'                            { neighbor_count += 1; } // Up
    if y > 0 && x < x_bound && lines[y-1][x+1] == '@'            { neighbor_count += 1; } // Up and Right
    // Check characters in the same row
    if x > 0 && lines[y][x-1] == '@'                  { neighbor_count += 1; } // Left
    if x < x_bound && lines[y][x+1] == '@'            { neighbor_count += 1; } // Right
    // Check characters in 3 squares below this character
    if y < y_bound && x > 0 && lines[y+1][x-1] == '@'       { neighbor_count += 1; } // Down and Left
    if y < y_bound && lines[y+1][x] == '@'                  { neighbor_count += 1; } // Down
    if y < y_bound && x < x_bound && lines[y+1][x+1] == '@' { neighbor_count += 1; } // Down and Right

    neighbor_count
}

fn remove_rolls(lines: &mut Vec<Vec<char>>, removable_rolls: &Vec<(usize, usize)>) {
    for roll in removable_rolls {
        let y = roll.0;
        let x = roll.1;
        lines[y][x] = '.';
    }
}

fn part_one(lines: &Vec<Vec<char>>) -> Result<u32> {
    let number_of_lines = lines.len();
    let length_of_line = lines[0].len();
    let mut acceptable_rolls = 0;
    for y in 0..number_of_lines {
        for x in 0..length_of_line {
            debug!("Checking index y: {y} x:{x}");
            if lines[y][x] == '@' {
                debug!("Character is an @");
                let neighbor_count = get_neighbor_count(lines, y, x);
                if neighbor_count < 4 {
                    debug!("Character index y:{y} x:{x}  has {neighbor_count} neighbors");
                    acceptable_rolls += 1;
                }
            }
        }
    }
    Ok(acceptable_rolls)
}

fn part_two(lines: &mut Vec<Vec<char>>) -> Result<u32> {
    let number_of_lines = lines.len();
    let length_of_line = lines[0].len();
    let mut total_rolls_removed: u32 = 0;
    let mut removable_rolls: Vec<(usize, usize)> = Vec::new();
    loop {
        let mut new_rolls_removed = 0;
        // Same thing as part one, but also need to keep track of the index and remove them all after the fact.
        for y in 0..number_of_lines {
            for x in 0..length_of_line {
                debug!("Checking index y: {y} x:{x}");
                if lines[y][x] == '@' {
                    debug!("Character is an @");
                    let neighbor_count = get_neighbor_count(lines, y, x);
                    if neighbor_count < 4 {
                        debug!("Character index y:{y} x:{x}  has {neighbor_count} neighbors");
                        new_rolls_removed += 1;
                        removable_rolls.push((y,x));
                    }
                }
            }
        }
        if new_rolls_removed == 0 { break; }
        // Now that I've gone over the whole picture. I need to remove the paper rolls and add that count to the answer
        total_rolls_removed += new_rolls_removed;
        remove_rolls(lines, &removable_rolls);
        debug!("After removal map look like\n\n{:?}", lines);
    }
    Ok(total_rolls_removed)
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let mut lines = read_lines(&args.path)?;
    debug!("lines\n\n{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&mut lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
