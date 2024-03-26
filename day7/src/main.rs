use std::cell::RefCell;
use std::rc::Rc;
use std::vec;

type RcCell<T> = Rc<RefCell<T>>;

type DirStack = Vec<RcCell<FS>>;

#[derive(Debug)]
enum FS {
    File(u64),
    Folder(String, Vec<RcCell<FS>>),
}

// Defining `Default` so that we can `.take()` from a RefCell
impl Default for FS {
    fn default() -> Self {
        FS::File(0)
    }
}

impl FS {
    fn get_size(&self) -> u64 {
        match self {
            Self::File(i) => *i,
            Self::Folder(_, subdirs) => {
                subdirs.iter().map(|d| d.as_ref().borrow().get_size()).sum()
            }
        }
    }

    fn is_folder(&self) -> bool {
        match self {
            FS::Folder(..) => true,
            FS::File(..) => false,
        }
    }

    fn file_from_str(size: &str) -> Self {
        Self::File(size.parse().expect("Size should be parsable as int"))
    }

    fn folder_from_str(dirname: &str) -> Self {
        Self::Folder(dirname.to_string(), vec![])
    }

    fn iter_subfolders(&self) -> Option<impl '_ + Iterator<Item = &RcCell<Self>>> {
        match self {
            Self::File(..) => None,
            Self::Folder(_, v) => Some(v.iter()),
        }
    }

    /// Get the subfolder of a folder with a given name.
    ///
    /// Returns `None` if the FS is actually a file, or doesn't have
    /// the given subdirectory within it.
    fn get_subfolder(&self, dirname: &str) -> Option<RcCell<Self>> {
        let subdirs = match self {
            FS::Folder(_, v) => v,
            _ => {
                return None;
            }
        };
        for dir in subdirs {
            match &*dir.as_ref().borrow() {
                FS::Folder(d, _) if d == dirname => return Some(dir.clone()),
                _ => {}
            }
        }
        None
    }

    fn add_file(&mut self, file: FS) {
        let FS::Folder(_, v) = self else { panic!() };
        v.push(RefCell::new(file).into())
    }
}
impl From<FS> for Rc<RefCell<FS>> {
    fn from(value: FS) -> Self {
        Rc::new(RefCell::new(value))
    }
}

fn cwd(dir_stack: &DirStack) -> Rc<RefCell<FS>> {
    dir_stack.last().unwrap().clone()
}

fn getdir(dir_stack: &DirStack, dirname: &str) -> Option<RcCell<FS>> {
    cwd(dir_stack).as_ref().borrow().get_subfolder(dirname)
}

fn parse_input(input: &str) -> RcCell<FS> {
    let mut words = vec![];
    let root: RcCell<FS> = FS::Folder("/".to_string(), vec![]).into();
    let mut dir_stack: Vec<Rc<RefCell<FS>>> = vec![root.clone()];

    for line in input.lines() {
        words.clear();
        words.extend(line.split_ascii_whitespace());
        match words.as_slice() {
            // noop, always the first line
            ["$", "cd", "/"] => {}

            // Exit the CWD, going up a level towards root
            ["$", "cd", ".."] => {
                assert!(dir_stack.len() > 1);
                dir_stack.pop();
            }

            // Enter the given directory
            ["$", "cd", dirname] => {
                let new_cwd = getdir(&dir_stack, dirname).expect("subfolder should exist");
                dir_stack.push(new_cwd);
            }

            // We're about to be told a bunch of directories, but we don't actually
            // need to do anything about this
            ["$", "ls"] => {}

            // We're being shown a directory that's in the CWD
            ["dir", dirname] => {
                let new_folder = FS::folder_from_str(dirname);
                cwd(&dir_stack).as_ref().borrow_mut().add_file(new_folder);
            }

            // We're being shown a file that's in the CWD
            [size, _] => {
                let new_file = FS::file_from_str(size);
                cwd(&dir_stack).as_ref().borrow_mut().add_file(new_file);
            }

            _ => unreachable!(),
        }
    }
    root
}

/// Given a filesystem, traverses it, returning a flat vector of
/// every folder and subfolder's size.
fn get_all_sizes(file_system: &FS) -> Vec<u64> {
    let Some(v) = file_system.iter_subfolders() else {
        // fs is a file, return an empty vec
        return vec![];
    };
    let mut own_size = 0;
    let mut sizes = vec![];
    for f in v {
        if f.as_ref().borrow().is_folder() {
            sizes.append(&mut get_all_sizes(&*f.as_ref().borrow()))
        }
        own_size += f.as_ref().borrow().get_size();
    }
    sizes.push(own_size);
    sizes
}

/// Given a file system, find all subdirectories of any level with a size of <=100_000,
/// and return the sum of their sizes.
fn part1(file_system: &FS) -> u64 {
    let all_sizes = get_all_sizes(&file_system);
    all_sizes.into_iter().filter(|x| *x <= 100_000).sum()
}

/// Find the size of the smallest subfolder such that total_used_space - subfolder <= 40_000_000
fn part2(file_system: &FS) -> u64 {
    let all_sizes = get_all_sizes(&file_system);
    let total_size = *all_sizes.iter().max().unwrap(); // root's size
    all_sizes
        .into_iter()
        .filter(|x| total_size - *x <= 40_000_000)
        .min()
        .unwrap()
}

fn main() {
    let input = include_str!("../input");
    let file_tree = parse_input(&input);

    let file_system = Rc::try_unwrap(file_tree).unwrap().take();

    // println!("{:#?}", ft);
    println!("Part 1: {}", part1(&file_system));
    println!("Part 2: {}", part2(&file_system));
}
