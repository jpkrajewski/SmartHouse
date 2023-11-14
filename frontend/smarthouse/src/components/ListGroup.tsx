interface ListGroupProps {
  items: string[];
  heading: string;
  onSelectItem: (item: string) => void;
}

function ListGroup({ items, heading, onSelectItem }: ListGroupProps) {
  return (
    <>
      <h1>{heading}</h1>
      <ul className="list-group">
        {items.map((item) => (
          <li className="list-group-item" onClick={() => onSelectItem(item)}>
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
