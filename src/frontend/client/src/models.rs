struct Book {
    id: u32,
    title: String,
    author: String,
    categories: Vec<String>,
    cover: bytes::Bytes,
    pages: u32,
    progress: u32,
    file_name: String,
    description: String,
    date: String,
    rights: String,
    tags: Vec<String>,
    identifier: String,
    publisher: String,
}

struct Collection {
    collection_id: u32,
    collection: String,
    books: Vec<Book>,
}
