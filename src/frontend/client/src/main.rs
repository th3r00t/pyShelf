use yew::prelude::*;
mod models;
use models::{Book, Collection};

#[function_component(App)]
fn app() -> Html {
    html! {
        <>
            <div>{ "pyShelf V: 0.7.1--dev" }</div>
        </>
    }
}

fn main() {
    yew::Renderer::<App>::new().render();
}
