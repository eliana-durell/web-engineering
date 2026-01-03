import { Component } from "react";
import { Container, Form, FormGroup, Label, Row, Col, Input, Button } from 'reactstrap';

class SingleFoodLabel extends Component {
    constructor (props) {
        super(props);
        this.state = {
            inputValues: { }
        };
    }

    submitItem = (e) => {
        e.preventDefault();
        let curr_nutrition_info = this.props.nutrition_dict[this.props.selected_item];
        let inputValues = this.state.inputValues;
        let newInputValues = { item: this.props.selected_item };
        Object.entries(inputValues).forEach(([key, value]) => {
            newInputValues[key] = value;  // add the inputted values to new input values
        });
        // to prevent unchanged values from being set to 0
        Object.entries(curr_nutrition_info).forEach(([key, value]) => {
            // check if key - name pair doesn't exist in inputValues
            if ( !(key in newInputValues) ) {
                newInputValues[key] = value;  // add the original values to new input values
            } 
        });
        
        this.props.onSubmitItem(newInputValues); 
        setTimeout(() => { //wait for updated values to render before resetting, else it flashes old value
            this.setState({ inputValues: {} });
        }, 150); 
    }

    handleChangeField = (e) => {
        let newInputValues = {...this.state.inputValues}; //create shallow copy
        newInputValues[e.target.name] = e.target.value;
        this.setState({inputValues: newInputValues});
    }

    render() {
        const item = this.props.selected_item;
        const nutrition = this.props.nutrition_dict[item];
        if (!item || !nutrition) {
            return (
            <Container className="no-form">
                <Label>Select an item to see nutrition facts.</Label>
            </Container>
            );
        }

        let totalFat_dv = Math.round((nutrition.totalFat / 78) * 100); //FDA recommended 78
        let saturatedFat_dv = Math.round((nutrition.saturatedFat / 20) * 100); //20
        let carbohydrate_dv = Math.round((nutrition.carbohydrate / 275) * 100); //275
        let protein_dv = Math.round((nutrition.protein / 50) * 100); //50

        return (
            <Form className="form form-btm" onSubmit={this.submitItem}>
                <h3 className="bold">Selected Nutrition Facts</h3>
                <p className="thin-line"></p>
                <FormGroup>
                    <p id="small-font">Amount per serving</p>
                    <Row>
                        <Label className="big-font" 
                            xxl={7} xl={7} lg={7} md={7} sm={7} xs={7}>
                            Calories
                        </Label>
                        <Col xxl={5} xl={5} lg={5} md={5} sm={5} xs={5}>
                            <Input className="big-font" name="calories" value={this.state.inputValues["calories"] ?? nutrition.calories}
                                                onChange={this.handleChangeField} type="number"/>
                        </Col>
                    </Row>
                </FormGroup>
                <p className="seperator"></p>
                <Label className="bold" 
                    xxl={{offset: 8, size: 4}} xl={{offset: 7, size: 5}} lg={{offset: 8, size: 4}}
                    md={{offset: 8, size: 4}} sm={{offset: 8, size: 4}}  xs={{offset: 7, size: 5}}>
                    % Daily Value
                </Label>
                <p className="thin-line"></p>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Label className="bold">Total Fat</Label>
                        </Col>
                        <Col className="line" xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Input className="grams" name="totalFat" value={this.state.inputValues["totalFat"] ?? Math.round(nutrition.totalFat)}
                                                    onChange={this.handleChangeField} type="number"/>
                            <Label className="measurement">g</Label>
                        </Col>
                        <Col xxl={{offset: 2, size: 2}} xl={{offset: 2, size: 2}} lg={{offset: 2, size: 2}}
                        md={{offset: 2, size: 2}} sm={{offset: 2, size: 2}} xs={{offset: 1, size: 2}}>
                            <Label className="bold">{totalFat_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={{offset:1, size: 4}} xl={{offset:1, size: 5}} lg={{offset:1, size: 5}}
                        md={{offset:1, size: 5}} sm={{offset:1, size: 5}} xs={{offset:1, size: 4}}>
                            <Label>Saturated Fat</Label>
                        </Col>
                        <Col className="line" xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Input className="grams" name="saturatedFat" value={this.state.inputValues["saturatedFat"] ?? Math.round(nutrition.saturatedFat)} 
                                            onChange={this.handleChangeField} type="number"/>
                            <Label className="measurement">g</Label>
                        </Col>
                        <Col xxl={{offset: 1, size: 2}} xl={{offset: 0, size: 2}} lg={{offset: 0, size: 2}}
                        md={{offset: 0, size: 2}}  sm={{offset: 0, size: 2}} xs={{offset: 0, size: 2}}>
                            <Label className="bold">{saturatedFat_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={{offset: 1, size: 3}} xl={{offset: 1, size: 4}} lg={{offset: 1, size: 4}}
                        md={{offset: 1, size: 4}} sm={{offset: 1, size: 4}} xs={{offset: 1, size: 4}}>
                            <Label><span className="italics">Trans</span> Fat</Label>
                        </Col>
                        <Col className="line" xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Input className="grams" name="transFat" value={this.state.inputValues["transFat"] ?? Math.round(nutrition.transFat)}
                                            onChange={this.handleChangeField} type="number"/>
                            <Label className="measurement">g</Label>
                        </Col>
                        <Col xxl={{offset: 2, size: 2}} xl={{offset: 2, size: 2}} lg={{offset: 2, size: 2}}
                        md={{offset: 2, size: 2}}  sm={{offset: 2, size: 2}} xs={{offset: 2, size: 2}}> 
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={6} xl={7} lg={7} md={7} sm={7} xs={5}> 
                            <Label className="bold">Total Carbohydrate</Label>
                        </Col>
                        <Col className="line" xxl={4} xl={3} lg={3} md={3} sm={3} xs={4}>
                            <Input className="grams" name="carbohydrate" value={this.state.inputValues["carbohydrate"] ?? Math.round(nutrition.carbohydrate)} 
                                            onChange={this.handleChangeField} type="number"/>
                            <Label className="measurement">g</Label>
                        </Col>
                        <Col xxl={{offset: 0, size: 2}} xl={{offset: 0, size: 2}} lg={{offset: 0, size: 2}}
                         md={{offset: 0, size: 2}} sm={{offset: 0, size: 2}} xs={{offset: 0, size: 2}}>
                            <Label className="bold">{carbohydrate_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row>
                        <Col xxl={3} xl={3} lg={3} md={3} sm={3} xs={3}>
                            <Label className="bold">Protein</Label>
                        </Col>
                        <Col className="line" xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Input className="grams" name="protein" value={this.state.inputValues["protein"] ?? Math.round(nutrition.protein)}
                                            onChange={this.handleChangeField} type="number"/>
                            <Label className="measurement">g</Label>
                        </Col>
                        <Col xxl={{offset: 3, size: 2}} xl={{offset: 3, size: 2}} lg={{offset: 3, size: 2}}
                        md={{offset: 3, size: 2}} sm={{offset: 3, size: 2}} xs={{offset: 2, size: 2}}>
                            <Label className="bold">{protein_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <p className="seperator"></p>
                <p>* The Daily Value (DV) tells you how much a nutrient in a serving of food contributes to a daily diet.2,000
                    calories a day is used for general nutrition advice.
                </p>
                <FormGroup row>
                    <Col xxl={{offset: 4,size: 7}} xl={{offset: 4,size: 7}} lg={{offset: 4,size: 7}}
                    md={{offset: 4,size: 7}}  sm={{offset: 4,size: 7}}  xs={{offset: 4,size: 7}}> 
                        <Button size="lg" color="success" type="submit">Save</Button>
                    </Col>
                </FormGroup>
            </Form>
        );
    }
}
export default SingleFoodLabel;