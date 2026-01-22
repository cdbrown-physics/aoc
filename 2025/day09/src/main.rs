use std::{path::{Path, PathBuf}};
use std::fs::File;
use std::io::{BufRead, BufReader};

use anyhow::{Context, Result};
use clap::Parser;
use log::{debug, info};

#[derive(Parser)]
struct Args{
    #[arg(long)]
    path: PathBuf,
}
#[derive(Debug)]
struct RedTile {
    x: u32,
    y: u32
}
impl RedTile {
    fn area(&self, other: &RedTile) -> u64 {
        let dx = self.x.abs_diff(other.x) + 1;
        let dy = self.y.abs_diff(other.y) + 1;
        let area: u64 = dx as u64 * dy as u64;
        area
    }
    fn green_line(&self, other: &RedTile) -> Vec<GreenTile> {
        let mut green_tiles: Vec<GreenTile> = Vec::new();
        if self.x.abs_diff(other.x) == 0 {
            // Then we have a horizontal line. Add Green tiles with self.x and all the difference y values
            // I need to get the largest of the two y values.
            if other.y > self.y {
                for green_y in (self.y+1)..other.y {
                    let green_tile = GreenTile{x: self.x, y: green_y};
                    green_tiles.push(green_tile);
                }
            }
            else {
                for green_y in (other.y + 1)..self.y {
                    let green_tile = GreenTile{x: self.x, y: green_y};
                    green_tiles.push(green_tile);
                }
            }
        }
        else if self.y.abs_diff(other.y) == 0 {
            /*Then we have a vertical line. Add Green tiles with self.y and all the different x values */
            if other.x > self.x {
                for green_x in (self.x+1)..other.x {
                    let green_tile = GreenTile{x: green_x, y: self.y};
                    green_tiles.push(green_tile);
                }
            }
            else {
                for green_x in (other.x + 1)..self.x {
                    let green_tile = GreenTile{x: green_x, y: self.y};
                    green_tiles.push(green_tile);
                }
            }
        }
        green_tiles
    }
}

#[derive(Debug)]
struct GreenTile {
    x: u32,
    y: u32
}
fn read_lines(filename: &Path) -> Result<Vec<RedTile>> {
    // Want to read in the data file and store the numbers in 
    let path = Path::new(filename);
    let file = File::open(path).context("Failed to open file")?;

    let reader = BufReader::new(file);
    let mut red_tiles: Vec<RedTile> = Vec::new();
    for line in reader.lines() {
        let tile_coordinates: Vec<u32> = line?.split(',')
            .map(|s| s
                    .trim()
                    .parse::<u32>()
                    .unwrap())
            .collect();
        debug!("Red Tile location is at {tile_coordinates:?}");
        let red_tile = RedTile{x: tile_coordinates[0], y: tile_coordinates[1]};
        red_tiles.push(red_tile);
    }
    Ok(red_tiles)
}

fn find_green_tiles(red_tiles: &[RedTile]) -> Result<Vec<GreenTile>> {
    let mut green_tiles: Vec<GreenTile> = Vec::new();
    // Start by adding all the tiles in a line. Go through the list of tiles and
    let last_tile = red_tiles[0]; // For starting we can just grab the first element in the red tile list
    for red_tile in red_tiles[1..] {
        let new_green_tiles: Vec<GreenTile> = last_tile.green_line(red_tile);
    }
}

fn part_one(red_tiles: &[RedTile]) -> Result<u64> {
    let mut largest_area = 0;
    // Need to find the rectagles of all the different combinations for the tiles. 
    let num_red_tiles = red_tiles.len();
    for red_tile_one_index in 0..num_red_tiles {
        for red_tile_two_index in (red_tile_one_index+1)..num_red_tiles {
            let area = red_tiles[red_tile_one_index].area(&red_tiles[red_tile_two_index]);
            debug!("Tiles {:?} and {:?}", red_tiles[red_tile_one_index], red_tiles[red_tile_two_index]);
            debug!("Gives an area of: {area}");
            if area > largest_area {
                largest_area = area;
            }
        }
    }
    Ok(largest_area)
}

fn part_two(red_tiles: &[RedTile]) -> Result<u64> {
    let mut largest_area = 0;
    let green_tiles: Vec<GreenTile> = find_green_tiles(red_tiles);
    Ok(largest_area)
}
fn main() -> Result<()> {
    env_logger::init();
    info!("Starting Program Day 09");
    let args = Args::parse();
    let red_tiles = read_lines(&args.path)?;
    debug!("Lines:\n\n{red_tiles:?}");
    let part_one_answer = part_one(&red_tiles)?;
    println!("Answer to part one is: {part_one_answer}");
    let part_two_answer = part_two(&red_tiles)?;

    Ok(())
}
