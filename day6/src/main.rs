fn main() {
    let input = include_bytes!("../input");
    for window_size in [4, 14] {
        let mut buffer = Vec::<u8>::with_capacity(window_size);
        for (i, window) in input.windows(window_size).enumerate() {
            buffer.extend(window);
            buffer.sort();
            buffer.dedup();
            if buffer.len() == window_size {
                println!("First unique sequence of {window_size} found at {:?}", i+window_size);
                break;
            }
            buffer.clear();
        }
    }
}
