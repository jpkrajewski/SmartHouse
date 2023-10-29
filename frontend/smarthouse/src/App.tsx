import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";

function App() {
  let props = {
    items: ["item1", "item2", "item3"],
    heading: "List Group"
  }
  const handleSelectItem = (item: string) => {
    console.log(item);
  }

  return (
    <div className="App">
      <Alert> Hello World </Alert>
      <Button />
      <ListGroup items={props.items} heading={props.heading} onSelectItem={handleSelectItem}/>
    </div>
  );
}

export default App;


