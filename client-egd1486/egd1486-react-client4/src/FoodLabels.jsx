import { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import SingleFoodLabel from './SingleFoodLabel.jsx';
import TotalFoodLabel from './TotalFoodLabel.jsx';

class FoodLabels extends Component {
    constructor (props) {
        super(props);
    }

    submitItem = (inputValues) => {
        this.props.onSubmitItem(inputValues);
    }

    render() {
        return(
            <Container>
                <Row>
                    <Col>
                        <SingleFoodLabel 
                        key={this.props.selected_item || 'none'}  //unmount and remount the component whenever key changes
                        nutrition_dict={this.props.nutrition_dict} 
                        selected_item={this.props.selected_item}
                        onSubmitItem={this.submitItem}/>
                    </Col>
                    <Col>
                        <TotalFoodLabel 
                        nutrition_dict={this.props.nutrition_dict}
                        selected_item_lst={this.props.selected_item_lst}/>
                    </Col>
                </Row>
            </Container>
        );
    }
}
export default FoodLabels;