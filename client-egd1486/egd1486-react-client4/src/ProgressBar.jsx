import { Component } from "react";
import { Container, Row, Col, Input, Progress } from 'reactstrap';

class ProgressBar extends Component {
    constructor(props) {
        super(props);
    }

    changeGoal = (e) => {
        this.props.onChangeGoal(e.target.value);
    }

    render() {
        const lst = this.props.selected_item_lst;
        const curr_nutrition_dict = this.props.nutrition_dict;
        if(lst == []) {
            return (
                <div></div>
            );
        }
        
        let calories = 0;
        lst.forEach(item => {
            let nutrition = curr_nutrition_dict[item];
            calories = calories + nutrition["calories"];
        });

        return (
            <Container className="progress-bar">
                <Row>
                    <Col xxl={10} xl={10} lg={10} md={12} sm={12} xs={12}>
                        <Progress max={this.props.calorie_goal} value={calories} className="bar"/>
                    </Col>
                    <Col xxl={{offset: 0, size: 2}} xl={{offset: 0, size: 2}} lg={{offset: 0, size: 2}}
                     md={{offset: 10, size: 2}} sm={{offset: 10, size: 2}} xs={{offset: 8, size: 4}}>
                        <Input value={this.props.calorie_goal} onChange={this.changeGoal}></Input>
                    </Col>
                </Row>
            </Container>
        );
    }

}
export default ProgressBar;