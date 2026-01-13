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
    x: f32,
    y: f32,
    z: f32,
    index: u32
}

impl JunctionBox {
    fn distance(&self, other: &JunctionBox) -> f32 {
        let dx = other.x - self.x;
        let dy = other.y - self.y;
        let dz = other.z - self.z;
        (dx.powf(2.0) + dy.powf(2.0) + dz.powf(2.0)).sqrt()
    }
    
}

#[derive(Debug)]
struct Distance<'a>{
    distance: f32,
    box_one: &'a JunctionBox,
    box_two: &'a JunctionBox
}

#[derive(Debug)]
struct Circuit {
    junction_box_ids: Vec<u32>
}

fn read_lines(filename: &Path) -> Result<Vec<Vec<f32>>> {
    /*For this problem I want to read in the file and store each line as a 
    tuple of numbers X,Y,Z and then we can use those values for each 'box' */
    let path = Path::new(filename);
    let file = File::open(path)?;

    let reader = BufReader::new(file);
    let mut lines = Vec::new();

    for line in reader.lines() {
        let line_content: Vec<f32> = line?.split(',').map(|s| s.trim().parse::<f32>().unwrap()).collect();
        debug!("Line contents are {line_content:?}");
        lines.push(line_content);
    }
    Ok(lines)
}

fn check_circuits(distance: &Distance, circuits: &[Circuit]) -> bool {
    // Check if the junction boxes in the distacne object passed in are in an existing circuit or not.
    let jb1_id = &distance.box_one.index;
    let jb2_id = &distance.box_two.index;
    for circuit_index in 0..circuits.len() {
        if circuits[circuit_index].junction_box_ids.contains(jb1_id) {
            /* Junction box 1 is in a circuit. Need to add the other junction box to this circuit. If that other 
            junction box is in a circuit, then the entire circuit needs to be connected. If the other junction box 
            isn't in any  other circuit, then just add it and move on. 
            
            I don't need to look back at other circuits just look at the rest of the circuits for the second box.*/
            for c2 in 
        } 
        else if circuits[circuit_index].junction_box_ids.contains(jb2_id) {
            /* Junction box 2 is in a circuit. Need to add the other junction box to this circuit. If that other 
            junction box is in a circuit, then the entire circuit needs to be connected. If the other junction box 
            isn't in any  other circuit, then just add it and move on. */
        }

    }
    false
}

fn part_one(lines: &[Vec<f32>]) -> Result<f32> {
    println!("{lines:?}");
    let mut junction_boxes: Vec<JunctionBox> = Vec::new();
    let mut index: u32 = 0;
    for line in lines {
        let jb = JunctionBox {x: line[0], y: line[1], z: line[2], index};
        junction_boxes.push(jb);
        index += 1;
    }
    println!("{junction_boxes:?}");
    // Now with all of the JunctionBox structs, need to find the distance between all members. And make a vector of 
    // those distances I already know how many distances I'll need, so I can make the distances vector with that many
    // elements. And then just add elements into that list.
    let jb_len = junction_boxes.len();
    println!("{jb_len}");
    let numbers_of_distances = jb_len*(jb_len - 1) / 2; // Elements in nxn matrix above diagonal.
    let mut distances: Vec<Distance> = Vec::with_capacity(numbers_of_distances);
    for jb_one_index in 0..jb_len {
        for jb_two_index in (jb_one_index+1)..jb_len {
            let dist = junction_boxes[jb_one_index].distance(&junction_boxes[jb_two_index]);
            let distance = Distance {distance: dist, box_one: &junction_boxes[jb_one_index], box_two: &junction_boxes[jb_two_index]};
            distances.push(distance);
        }
    }
    debug!("***\n\nDistances pre sort: {distances:?}");
    // Now I want to sort distances based on the distance element. 
    distances.sort_by(|a,b| a.distance.total_cmp(&b.distance));
    debug!("*****\n\nDistances post sort: {distances:?}");
    let mut circuits: Vec<Circuit> = Vec::new();
    for d in 0..10 {
        let distance = &distances[d];
        if check_circuits
    }
    Ok(0.0)
}

fn part_two(lines: &[Vec<f32>]) -> Result<f32> {
    Ok(0.0)
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
