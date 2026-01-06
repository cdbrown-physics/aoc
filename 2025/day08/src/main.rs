use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result};
use clap::Parser;
use log::{debug, info, warn};

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}

// Junction box struct
#[derive(Debug)]

struct JunctionBox {
    x: u32,
    y: u32,
    z: u32,
    index: u32
}

#[derive(Debug)]
struct Circuit {
    junction_boxs: Vec<u32>
}

fn read_lines(filename: &Path) -> Result<Vec<Vec<u32>>> {
    /*For this problem I want to read in the file and store each line as a 
    tuple of numbers X,Y,Z and then we can use those values for each 'box' */
    let path = Path::new(filename);
    let file = File::open(path)?;

    let reader = BufReader::new(file);
    let mut lines = Vec::new();

    for line in reader.lines() {
        let line_content: Vec<u32> = line?.split(',').map(|s| s.trim().parse::<u32>().unwrap()).collect();
        debug!("Line contents are {line_content:?}");
        lines.push(line_content);
    }
    Ok(lines)
}

fn part_one(lines: &[Vec<u32>]) -> Result<u32> {
    /*Planned steps
    1.  */
    println!("{lines:?}");
    let mut junction_boxes: Vec<JunctionBox> = Vec::new();
    let mut index: u32 = 0;
    for line in lines {
        let jb = JunctionBox {x: line[0], y: line[1], z: line[2], index};
        index += 1;
        junction_boxes.push(jb);
    }
    println!("{junction_boxes:?}");
    Ok(0)
}

fn part_two(lines: &[Vec<u32>]) -> Result<u32> {
    Ok(0)
}

fn main() -> Result<()> {
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let mut lines = read_lines(&args.path)?;
    debug!("lines\n\n{:?}", lines);
    let part_one_answer = part_one(&lines)?;
    println!("Answer to part one: {part_one_answer}");
    let part_two_answer = part_two(&lines)?;
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
