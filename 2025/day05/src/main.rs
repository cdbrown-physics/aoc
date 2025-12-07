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

fn read_lines(filename: &Path)-> Result<(Vec<(u64, u64)>, Vec<u64>)> {
    let file = File::open(filename).context("Failed to open the file")?;
    let reader = BufReader::new(file);
    let mut range_lines: Vec<(u64, u64)> = Vec::new();
    let mut ingredient_id_num: Vec<u64> = Vec::new();
    let mut ingredient_parse: bool = false;
    for line in reader.lines() {
        let line_value: String = line?;
        debug!("Parsing line {:?}", line_value);
        if line_value.is_empty() {
            ingredient_parse = true;
            continue;
        }
        if ingredient_parse {
            ingredient_id_num.push(line_value.trim().parse::<u64>()?);
        }
        else {
            let tmp_vec_string: Vec<String> = line_value.split('-').map(|s| s.trim().to_string()).collect();
            let range_start = tmp_vec_string[0].parse::<u64>().context("Failed to parse {tmp_vec_string[0]}")?;
            let range_end = tmp_vec_string[1].parse::<u64>().context("Failed to parse {tmp_vec_string[1]}")?;
            range_lines.push((range_start, range_end));
        }
    }
    Ok((range_lines, ingredient_id_num))
}

fn part_one(range_ids: &[(u64, u64)], food_ids: &[u64]) -> u32
{
    let mut number_of_acceptable_foods: u32 = 0;
    for &id in food_ids {
        for range in range_ids {
            if id >= range.0 && id <= range.1 {
                // food id is in an acceptable range
                debug!("Food id {id} is acceptable");
                number_of_acceptable_foods += 1;
                break
            }
        }
    }
    number_of_acceptable_foods
}

fn part_two(range_ids: &mut Vec<(u64, u64)>) -> u64 {
    /*Game plan: Sort the list of id ranges, then just look at the last set. If the next one overlaps, just add the 
    remainder. If no overlap, then just add that whole range */
    range_ids.sort_by_key(|(a, _)| *a);
    debug!("Sorted acceptable ids {range_ids:?}");
    let mut total_ids: u64 = 0;
    let mut last_id_range: (u64, u64) = (0, 0);
    for &(start, end) in range_ids.iter() {
        debug!("Looking at range {start} - {end}");
        if start > last_id_range.1 && end >= start {
            // whole new range to look at
            debug!("Whole new range to add");
            total_ids += end - start + 1; // supid off by 1
            debug!("New range adding {}", end-start+1);
            last_id_range = (start, end)
        }
        else if start == last_id_range.0 && end < last_id_range.1 {
            debug!("Subset of last range. Nothing to add");
            continue;
        }
        else if start > last_id_range.0 && end < last_id_range.1 {
            debug!("Subset of last range. Nothing to add");
            continue;
        }
        else if start == last_id_range.0 && start == last_id_range.1 && end > last_id_range.1 {
            debug!("Adding range, -1 because start overlaps with last range");
            total_ids += end - start;
            last_id_range = (start, end);
        }
        else if start == last_id_range.1 && end == last_id_range.1{
            continue;
        }
        else if start > last_id_range.0 && end == last_id_range.1 {
            continue
        }
        else if start < last_id_range.1 && end > last_id_range.1 {
            // Minor overlap just add extra 
            total_ids += end - last_id_range.1;
            debug!("Minor overlap adding {}", end-last_id_range.1);
            last_id_range = (start, end);
        }
        else if start == last_id_range.1 && end > last_id_range.1 {
            debug!("Last number overlap adding new range with out the extra 1");
            total_ids += end - start; 
            debug!("New range adding {}", end-start+1);
            last_id_range = (start, end)
        }
        else if start == last_id_range.0 && end > last_id_range.1 {
            total_ids += end - last_id_range.1;
            debug!("Minor overlap adding {}", end-last_id_range.1);
            last_id_range = (start, end);
        }
        else if start == last_id_range.0 && end == last_id_range.1 {
            debug!("Total overlap.");
            continue;
        }
        else {
            warn!("Other odd case, look here to see how to handel it!");
            debug!("Current start end: {start} - {end}");
            debug!("Last range: {last_id_range:?}");
        }
    }
    total_ids
}

fn main() -> Result<()>
{
    env_logger::init();
    info!("Starting program");
    let args = Args::parse();
    let (ranges, food_ids) = read_lines(&args.path)?;
    debug!("Ragnes\n\n{:?}", ranges);
    debug!("Food Id's: {:?}", food_ids);
    let part_one_answer = part_one(&ranges, &food_ids);
    println!("Answer to part one: {part_one_answer}");
    let mut ranges_copy = ranges.clone();
    let part_two_answer = part_two(&mut ranges_copy);
    println!("Answer to part two: {part_two_answer}");
    Ok(())
}
