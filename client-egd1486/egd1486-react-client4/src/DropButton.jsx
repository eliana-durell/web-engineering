import { Component } from "react";
import { Container, Row, Button } from "reactstrap";

class DropButton extends Component {
    constructor(props) {
        super(props);
    }

    removeItem = (e) => {
        this.props.onRemoveItem();
    }

    render() {
        return(
            <Container>
                <Row>
                    <p></p>
                </Row>
                <Row>
                    <Button color="primary" outline onClick={this.removeItem} id="btn">&lt;&lt;</Button>
                </Row>
            </Container>
        );
    }
}
export default DropButton;