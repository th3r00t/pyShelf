use yew::prelude::*;

#[function_component(App)]
fn app() -> Html {
    html! {
        // <div>
        //     <h1>{ "Hello World!" }</h1>
        // </div>
        <>
            <div>{ "pyShelf V: 0.7.1--dev" }</div>
        </>
    }
}

fn main() {
    yew::Renderer::<App>::new().render();
}
