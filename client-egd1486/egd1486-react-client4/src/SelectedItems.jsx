import { Component } from "react";
import { Container } from "reactstrap";

class SelectedItems extends Component {
    constructor(props) {
        super(props);
    }

    removeSelect = (e) => {
        let selected_item = e.target.value;
        let selected_item_idx = e.target.selectedIndex;
        this.props.onRemoveSelect(selected_item, selected_item_idx);
    }

    render() {
        let selectedItems = this.props.selected_item_lst.map((item, idx) => 
            <option value={item} key={`${item}-${idx}`}>
                {item}
            </option>
        );

        return(
            <Container className="menu">
                <label htmlFor="selected-items">Selected items</label>
                <select id="selected-items" multiple onChange={this.removeSelect}>
                        {selectedItems}
                </select>
            </Container>
        );
    }
}
export default SelectedItems;