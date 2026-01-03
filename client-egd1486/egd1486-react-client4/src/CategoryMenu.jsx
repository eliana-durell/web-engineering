import { Component } from "react";
import { Container, Row, Col } from "reactstrap";

class CategoryMenu extends Component {
    constructor(props) {
        super(props);
    }

    changeCategoryMenu = (e) => 
    { //event target is automatically passed as param
        let new_category = e.target.value; //get selected category
        this.props.onChangeCategoryMenu(new_category);
    }       
    
    render() {
        return (
            <Container className="menu">
                <label htmlFor="categories">Categories</label>
                <select id="categories" onChange={this.changeCategoryMenu}>
                    <option value={this.props.category_lst[0]}>{this.props.category_lst[0]}</option>
                    <option value={this.props.category_lst[1]}>{this.props.category_lst[1]}</option>
                    <option value={this.props.category_lst[2]}>{this.props.category_lst[2]}</option>
                    <option value={this.props.category_lst[3]}>{this.props.category_lst[3]}</option>
                    <option value={this.props.category_lst[4]}>{this.props.category_lst[4]}</option>
                </select>
            </Container>
        );
    }
}
export default CategoryMenu;