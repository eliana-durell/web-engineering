import { Component } from "react";
import { Container, Row, Col, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class MenuItems extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modal: false,
            inputValues: { }
        }
    }
    
    addSelect = (e) => {
        let selected_item = e.target.value;
        this.props.onAddSelect(selected_item, null);
    }

    setModal = (e) => {
        this.setState({modal: !this.state.modal});
    }

    deleteItem = (e) => {
        this.props.onDeleteItem();
    }

    submitNewItem = (e) => {
        e.preventDefault();
        this.props.onSubmitNewItem(this.state.inputValues); 
        // setTimeout(() => {
        //     this.setState({modal: !this.state.modal, inputValues: {} }); //reset fields
        // }, 150);
        this.setState({modal: !this.state.modal, inputValues: {} });
    }

    handleChangeField = (e) => {
        let newInputValues = {...this.state.inputValues}; //create shallow copy
        newInputValues[e.target.name] = e.target.value;
        this.setState({inputValues: newInputValues});
    }

    render() {
        let menuItems = this.props.current_items.map(item => 
            <option value={item} key={item}>
                {item}
            </option>
        );

        return (
            <Container className="menu">
                    <label htmlFor="menu-items">Menu Items</label>
                    <select id="menu-items" multiple onClick={this.addSelect}>
                        {menuItems}
                    </select>
                    <Button color="dark" outline className="add-btn" onClick={this.setModal}>Add new item</Button>
                    <Button color="danger" outline className="add-btn" onClick={this.deleteItem}>Delete item</Button>
                <Modal isOpen={this.state.modal} toggle={this.setModal}>
                    <ModalHeader toggle={this.setModal}>Add a new item</ModalHeader>
                    <ModalBody>
                        <form onSubmit={this.submitNewItem}>
                            <p>
                                Item:
                                <input name="item" onChange={this.handleChangeField} required></input>
                            </p>
                            <p>Calories: 
                                <input name="calories" onChange={this.handleChangeField} type="number" required></input>
                            </p>
                            <p>
                                Total Fat:
                                <input name="totalFat" onChange={this.handleChangeField} type="number" required></input>g
                            </p>
                            <p>
                                Saturated Fat:  
                                <input name="saturatedFat" onChange={this.handleChangeField} type="number" required></input>g
                            </p>
                            <p>
                                Trans Fat: 
                                <input name="transFat" onChange={this.handleChangeField} type="number"required></input>g
                            </p>
                                <p>
                                Total Carbohydrate: 
                                <input name="carbohydrate" onChange={this.handleChangeField} type="number"required></input>g
                            </p>
                            <p>
                                Protein: 
                                <input name="protein" onChange={this.handleChangeField} type="number"required></input>g
                            </p>
                            <ModalFooter>
                            <Button color="success" type="submit">Save</Button>
                            {' '}
                            <Button color="danger" onClick={this.setModal}>Cancel</Button>
                            </ModalFooter>
                        </form>
                    </ModalBody>
                </Modal>
            </Container>
        );
    }
}
export default MenuItems;