import { Component } from "react";
import { Container, Row, Col, Button } from 'reactstrap';

class AddButton extends Component {
    constructor(props) {
        super(props);
    }

    addItem = (e) => {
        this.props.onAddItem();
    }

    render() {
        return(
            <Container className="menu button-space">
                <Row>
                    <p></p>
                </Row>
                <Row>
                    <Button color="primary" outline onClick={this.addItem}>&gt;&gt;</Button>
                </Row>
            </Container>
        );
    }
}
export default AddButton;