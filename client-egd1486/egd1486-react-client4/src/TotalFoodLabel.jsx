import { Component } from "react";
import { Form, FormText, FormGroup, Label, Row, Col, Input, Button } from 'reactstrap';


class TotalFoodLabel extends Component {
    constructor (props) {
        super(props);
    }

    render() {
        const lst = this.props.selected_item_lst;
        const nutrition_dict = this.props.nutrition_dict;
        if(lst == []) {
            return (
                <div>
                    <Label>Select an item to see total nutrition facts.</Label>
                </div>
                );
        }
        
        let calories = 0;
        let totalFat = 0;
        let saturatedFat = 0;
        let transFat = 0;
        let carbohydrate = 0;
        let protein = 0;

        lst.forEach(item => {
            let nutrition = nutrition_dict[item];
            calories = calories + nutrition["calories"];
            totalFat = totalFat + nutrition["totalFat"];
            saturatedFat = saturatedFat + nutrition["saturatedFat"];
            transFat = transFat + nutrition["transFat"];
            carbohydrate = carbohydrate + nutrition["carbohydrate"];
            protein = protein + nutrition["protein"];
        });

        let totalFat_dv = Math.round((totalFat / 78) * 100); //FDA recommended 78
        let saturatedFat_dv = Math.round((saturatedFat / 20) * 100); //20
        let carbohydrate_dv = Math.round((carbohydrate / 275) * 100); //275
        let protein_dv = Math.round((protein / 50) * 100); //50

        let fatColor = null;
        let satFatColor = null;
        let transFatColor = null;
        let carbColor = null;
        let proteinColor = null;
        if( totalFat > 78) {
            fatColor = "highlight";
        }
        if (saturatedFat > 20) {
            satFatColor = "highlight"
        }
        if (carbohydrate > 275) {
            carbColor = "highlight";
        }
        if (protein > 50) {
            proteinColor = "highlight";
        }
                
        return (
            <Form className="form form-btm">
                <h3 className="bold">Total Nutrition Facts</h3>
                <p className="thin-line"></p>
                <FormGroup>
                    <p id="small-font">Amount per serving</p>
                    <Row>
                        <Label className="big-font" 
                            xxl={7} xl={8} lg={8} md={8} sm={8} xs={8}>
                            Calories
                        </Label>
                        <Label className="big-font"
                             xxl={5} xl={4} lg={4} md={4} sm={4} xs={4}>
                            {calories}
                        </Label>
                    </Row>
                </FormGroup>
                <p className="seperator"></p>
                <Label className="bold"
                    xxl={{offset: 8, size: 4}} xl={{offset: 7, size: 5}} lg={{offset: 8, size: 4}}
                    md={{offset: 8, size: 4}} sm={{offset: 8, size: 4}} xs={{offset: 7, size: 5}}>
                    % Daily Value
                </Label>
                <p className="thin-line"></p>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Label className="bold">Total Fat</Label>
                        </Col>
                        <Col xxl={4} xl={4} lg={4} md={4} sm={4} xs={4}>
                            <Label className={fatColor}>{Math.round(totalFat)}g</Label>
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
                        md={{offset:1, size: 5}} sm={{offset:1, size: 5}} xs={{offset:1, size: 5}}>
                            <Label>Saturated Fat</Label>
                        </Col>
                        <Col xxl={3} xl={3} lg={3} md={3} sm={3} xs={2}> 
                            <Label className={satFatColor}>{Math.round(saturatedFat)}g</Label>
                        </Col>
                        <Col xxl={{offset: 2, size: 2}} xl={{offset: 1, size: 2}} lg={{offset: 1, size: 2}}
                        md={{offset: 1, size: 2}} sm={{offset: 1, size: 2}} xs={{offset: 1, size: 2}}>
                            <Label className="bold">{saturatedFat_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row className="btm-border">
                        <Col  xxl={{offset: 1, size: 3}} xl={{offset: 1, size: 4}} lg={{offset: 1, size: 4}}
                         md={{offset: 1, size: 4}} sm={{offset: 1, size: 4}} xs={{offset: 1, size: 4}}>
                            <Label><span className="italics">Trans</span> Fat</Label>
                        </Col>
                        <Col xxl={3} xl={3} lg={3} md={3} sm={3} xs={3}>
                            <Label className={transFatColor}>{Math.round(transFat)}g</Label>
                        </Col>
                        <Col xxl={{offset: 2, size: 2}} xl={{offset: 2, size: 2}} lg={{offset: 2, size: 2}}
                        md={{offset: 2, size: 2}} sm={{offset: 2, size: 2}} xs={{offset: 2, size: 2}}>
                            <Label></Label>
                        </Col>
                    </Row>
                </FormGroup>
                <FormGroup>
                    <Row className="btm-border">
                        <Col xxl={6} xl={7} lg={7} md={7} sm={7} xs={7}>
                            <Label className="bold">Total Carbohydrate</Label>
                        </Col>
                        <Col xxl={3} xl={3} lg={3} md={3} sm={3} xs={2}>
                            <Label className={carbColor}>{Math.round(carbohydrate)}g</Label>
                        </Col>
                        <Col xxl={{offset: 1, size: 2}} xl={{offset: 0, size: 2}} lg={{offset: 0, size: 2}}
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
                        <Col xxl={3} xl={3} lg={3} md={3} sm={3} xs={3}>
                            <Label className={proteinColor}>{Math.round(protein)}g</Label>
                        </Col>
                        <Col  xxl={{offset: 4, size: 2}} xl={{offset: 4, size: 2}} lg={{offset: 4, size: 2}}
                        md={{offset: 4, size: 2}} sm={{offset: 4, size: 2}} xs={{offset: 3, size: 2}}>
                            <Label className="bold">{protein_dv}%</Label>
                        </Col>
                    </Row>
                </FormGroup>
                <p className="seperator"></p>
                <p>* The Daily Value (DV) tells you how much a nutrient in a serving of food contributes to a daily diet.2,000
                    calories a day is used for general nutrition advice.
                </p>
            </Form>
        );
    }
}
export default TotalFoodLabel;