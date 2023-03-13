use bytes::Bytes;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug)]
pub struct Book {
    book_id: i32,
    title: String,
    author: Option<String>,
    categories: Option<String>,
    cover: Option<Bytes>,
    pages: Option<i32>,
    progress: Option<f32>,
    file_name: String,
    description: Option<String>,
    date: String,
    rights: Option<String>,
    tags: Option<String>,
    identifier: Option<String>,
    publisher: Option<String>,
}

pub struct Collection {
    collection_id: i32,
    collection: String,
    books: Vec<Book>,
}
