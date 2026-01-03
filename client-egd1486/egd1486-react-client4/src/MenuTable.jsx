import { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import CategoryMenu from './CategoryMenu.jsx';
import MenuItems from './MenuItems.jsx';
import AddButton from './AddButton.jsx';
import DropButton from './DropButton.jsx';
import SelectedItems from './SelectedItems.jsx';

class MenuTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            whichMenu: "Menu"
        };
    }
    changeCategoryMenu = (new_category) => { 
        let new_menu_lst = this.props.menu_dict[new_category]; //get the new menu item list
        this.props.onCategoryMenuChange(new_category, new_menu_lst)
    } 

    addSelect = (item) => { // like removeSelect
        this.props.onChangeSelect(item);
        this.setState({whichMenu: "Menu"});
    }

    deleteItem = (idx) => {
        this.props.onDeleteItem(idx);
    }

    submitNewItem = (inputValues) => {
        this.props.onSubmitNewItem(inputValues);
    }

    handleAddItem = () => {
        if (this.state.whichMenu == "Menu")
        {
            let new_item_lst = [...this.props.selected_item_lst];
            let item_selected = this.props.selected_item; 
            if (!item_selected) { //check that there is an item selected
                return;
            }
            let nutrition_dict = this.props.nutrition_dict;
            let selected_item_calorie = nutrition_dict[item_selected]["calories"];
            let curr_calorie_total = this.state.total_calories;
            let new_calorie_total = curr_calorie_total;
            //add new item 
            new_item_lst.push(item_selected);
            // calculate calories
            new_calorie_total = curr_calorie_total + selected_item_calorie;

            //update selected item list and total calories
            this.props.onUpdateSelected(new_item_lst);
            this.setState({total_calories: new_calorie_total});  
        }
    }

    handleRemoveItem = () => {
        if (this.state.whichMenu == "Select")
        {
            let new_item_lst = [...this.props.selected_item_lst];
            let item_selected = this.props.selected_item; 
            if (!item_selected) { //check that there is an item selected
                return;
            }
            let nutrition_dict = this.props.nutrition_dict;
            let selected_item_calorie = nutrition_dict[item_selected]["calories"];
            let curr_calorie_total = this.state.total_calories;
            let new_calorie_total = curr_calorie_total; //no change to calories
            //remove the item at the index
            new_item_lst.splice(this.props.selected_item_idx, 1);
            // calculate calories
            new_calorie_total = curr_calorie_total - selected_item_calorie;

            //update selected item list and total calories
            this.props.onUpdateSelected(new_item_lst);
            this.setState({total_calories: new_calorie_total});  
        }
    }

    removeSelect = (item, idx) => { // like AddSelect
        this.props.onChangeSelect(item, idx);
        this.setState({whichMenu: "Select"});
    }

    render() {
        return(
            <Container>
                <Row>
                    <Col xxl={{offset: 0, size: 3}} xl={{offset: 0, size: 3}} lg={{offset: 1, size: 2}}
                        md={{offset: 2, size: 4}} sm={{offset: 2, size: 4}} xs={{offset: 2, size: 8}}>
                        <CategoryMenu 
                        category_lst={this.props.category_lst}
                        onChangeCategoryMenu={this.changeCategoryMenu}/>
                    </Col>
                    <Col xxl={{offset: 0, size: 3}} xl={{offset: 0, size: 3}} lg={{offset: 0, size: 3}} 
                        md={{offset: 0, size: 4}} sm={{offset: 0, size: 4}} xs={{offset: 2, size: 8}}>
                        <MenuItems 
                        key={this.props.current_items}
                        current_items={this.props.current_items} 
                        onAddSelect={this.addSelect} 
                        onDeleteItem={this.deleteItem}
                        onSubmitNewItem={this.submitNewItem}/>
                    </Col>
                    <Col xxl={{offset: 0, size: 2}} xl={{offset: 0, size: 2}} lg={{offset: 0, size: 2}} 
                        md={{offset: 2, size: 4}} sm={{offset: 2, size: 4}} xs={{offset: 2, size: 8}}>
                        <AddButton 
                        onAddItem={this.handleAddItem}/>
                        <DropButton 
                        onRemoveItem={this.handleRemoveItem}/>
                    </Col>
                    <Col xxl={{offset: 0, size: 4}} xl={{offset: 0, size: 4}} lg={{offset: 0, size: 4}}
                        md={{offset: 0, size: 6}} sm={{offset: 0, size: 6}} xs={{offset: 2, size: 8}}>
                        <SelectedItems 
                        selected_item_lst={this.props.selected_item_lst}
                        onRemoveSelect={this.removeSelect} /> 
                    </Col>
                </Row>
            </Container>
        );
    }
}
export default MenuTable;