import { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import Heading from "./Heading.jsx";
import MenuTable from "./MenuTable.jsx";
import ProgressBar from "./ProgressBar.jsx";
import FoodLabels from './FoodLabels.jsx';

class FoodPlannerTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
                category: "Proteins",
                category_lst: [],
                menu_dict: {},
                selected_item: null,
                selected_item_idx: null,
                selected_item_lst: [],
                calorie_goal: 2000,
                nutrition_dict: ""
                };
    }

     componentDidMount() {
        this.fetchData();
     }
     fetchData = () => {
        fetch('https://nutrikit-api.onrender.com/api/nutrition_api')
            .then((response) => {
                    if (response.status === 200) {
                        return (response.json());
                    } else {
                        console.log("HTTP error:" + response.status + ":" + response.statusText);
                        return ([["status ", response.status]]);
                    }
                }
            ) //The promise response is returned, then we extract the json data
            .then((jsonOutput) => //jsonOutput now has result of the data extraction
            {   //array containing arrays
                let new_category_lst = [];
                let new_menu_dict = {};
                let new_nutrition_dict = {};
                let prev_category = null;
                let item_lst = []

                for(let i = 0; i < jsonOutput.length; i++) {
                    let arr = jsonOutput[i];
                    //get categories and items in that category
                    let curr_category = arr[7];
                    if (curr_category != prev_category) {
                        new_category_lst.push(curr_category);
                        //done adding items to category
                        if (prev_category != null) //initial case: curr=protein, prev=null - don't add till curr=fruit, prev=protein
                        {
                            new_menu_dict[prev_category] = item_lst;
                            item_lst = [] //reset
                        }
                    }
                    //get items for each category
                    item_lst.push(arr[0])
                    if (i == jsonOutput.length-1) { //add grains 
                        new_menu_dict[prev_category] = item_lst;
                    }
                    //add item to nutrition dict - Parse into a dict containing str: dict
                    let item = arr[0];
                    let nutrition_info = {
                        "calories": arr[1], 
                        "totalFat": arr[2], 
                        "saturatedFat": arr[3],
                        "transFat": arr[4],
                        "protein": arr[5],
                        "carbohydrate": arr[6] };
                    new_nutrition_dict[item] = nutrition_info;
                    prev_category = curr_category; //update
                }
                this.setState({category_lst: new_category_lst,
                         menu_dict: new_menu_dict, nutrition_dict: new_nutrition_dict});
            })
            .catch((error) => {
                console.log(error);
                this.updateData("");
            })
    }
    updateData = (apiResponse) => {
        this.setState({ nutrition_dict: apiResponse })
    }

    handleCategoryMenuChange = (new_category, new_menu_lst) => {
        this.setState({ category: new_category, current_items: new_menu_lst });
    }

    handleDeleteItem = (e) => {
        fetch(`https://nutrikit-api.onrender.com/api/nutrition_api?item=${this.state.selected_item}`, {
                method: 'DELETE',
                headers: { 'Content-type': 'application/json; charset=UTF-8'}
        }).then(response => {
                if(response.status === 200) {
                     return (response.json());
                } else {
                    console.log("HTTP error:" + response.status + ":" + response.statusText);
                     return ([["status ", response.status]]);
                }
        }).then(jsonOutput => {
                // change nutrition table
                let new_nutrition_dict = { ...this.state.nutrition_dict };
                delete new_nutrition_dict[this.state.selected_item];
                let curr_item = this.state.selected_item;
                // get rid of item in menu_dict
                let new_menu_dict = { ...this.state.menu_dict };
                let category_item_lst = new_menu_dict[this.state.category];
                let new_category_item_lst = [];
                for(let i = 0; i<category_item_lst.length; i++) {
                        if(category_item_lst[i] !== curr_item) {
                                new_category_item_lst.push(category_item_lst[i]);
                        }
                }
                new_menu_dict[this.state.category] = new_category_item_lst;
                // get rid of it in selected_item_lst if exists
                let curr_selected_items = this.state.selected_item_lst;
                let new_selected_items = [];
                if (curr_selected_items.includes(curr_item)) {
                        for (let i = 0; i<curr_selected_items.length; i++) {
                                if(curr_selected_items[i] != curr_item) {
                                        new_selected_items.push(curr_selected_items[i]);
                                }
                        }
                        this.setState({nutrition_dict: new_nutrition_dict, menu_dict: new_menu_dict, 
                                selected_item_lst: new_selected_items, selected_item: null});
                } else {
                    // change selected_item to null
                    this.setState({nutrition_dict: new_nutrition_dict, menu_dict: new_menu_dict, selected_item: null});
                }
                this.fetchData(); //re render ui
        }).catch(error => {
                console.log(error);
                this.updateData("");
        })  
    }

    handleSubmitNewItem = (inputValues) => {
        let newInputValues = { 
                ...inputValues,      
                category: this.state.category   
        };
        fetch('https://nutrikit-api.onrender.com/api/nutrition_api', {
                method: 'POST',
                body: JSON.stringify(newInputValues),
                headers: { "Content-type": "application/json; charset=UTF-8" }
        }).then(response => {
                if(response.status === 200) {
                     return (response.json());
                } else {
                    console.log("HTTP error:" + response.status + ":" + response.statusText);
                     return ([["status ", response.status]]);
                }
        }).then(jsonOutput => {
                //update nutrition_dict
                let new_nutrition_dict = { ...this.state.nutrition_dict }; //create shallow copy
                let new_item = jsonOutput["item"].trim().toLowerCase(); //str
                // check if item already in 
                if (new_item in new_nutrition_dict) {
                        alert("Item already exists!");
                        return;
                }
                //get all nutrition info
                let item_info = {};
                Object.entries(jsonOutput).map(([name, value]) => {
                        if (name !== "item") {
                                item_info[name] = parseFloat(value);
                        }
                });
                new_nutrition_dict[new_item] = item_info;
                //update menu_dict
                let curr_category = this.state.category;
                let new_menu_dict = { ...this.state.menu_dict };
                let new_category_item_lst = [...this.state.menu_dict[curr_category]];
                new_category_item_lst.push(new_item);
                new_menu_dict[curr_category] = new_category_item_lst;
                
                this.setState({ nutrition_dict: new_nutrition_dict, menu_dict: new_menu_dict });
                this.fetchData(); //re render ui
        }).catch(error => {
                console.log(error);
                this.updateData("");
        })
    }

    handleUpdateSelected = (new_item_lst) => {
        this.setState({ selected_item_lst: new_item_lst});
    }

    handleChangeSelect = (new_selected_item, new_idx) => {
        this.setState({ selected_item: new_selected_item, selected_item_idx: new_idx });
    }

    handleChangeGoal = (value) => {
        this.setState({ calorie_goal: value });
    }

    handleSubmitItem = (inputValues) => {
        fetch('https://nutrikit-api.onrender.com/api/nutrition_api', {
                method: 'PUT',
                body: JSON.stringify(inputValues),
                headers: { "Content-type": "application/json; charset=UTF-8" }
        }).then((response) => {
                if (response.status === 200) {
                        return (response.json());
                } else {
                        console.log("HTTP error:" + response.status + ":" + response.statusText);
                        return ([["status ", response.status]]);
                }
        }).then(jsonOutput => {
                let new_nutrition_dict = { ...this.state.nutrition_dict }; //create shallow copy
                let curr_selected_item = this.state.selected_item;
                let item_dict = { ...new_nutrition_dict[curr_selected_item] }; //get nutrition info for item
                Object.entries(jsonOutput).forEach(([name, value]) => {
                if (value !== null && value !== undefined && !isNaN(value)) {
                        item_dict[name] = parseFloat(value);
                }
                });
                new_nutrition_dict[curr_selected_item] = item_dict; //update nutrition info for item
                
                this.updateData(new_nutrition_dict);
                this.fetchData(); //re render ui
        }).catch((error) => {
                console.log(error);
                this.updateData("");
        })
    }

    render() {
       return(
            <Container>
                <Row>
                     <Heading />
                </Row>
                <Row>
                    <Col xxl={{offset: 1, size: 11}} xl={{offset: 0, size: 12}} lg={{offset: 0, size: 12}} 
                     md={{offset: 0, size: 12}} sm={{offset: 0, size: 12}} xs={{offset: 0, size: 12}}>
                        <MenuTable 
                                category={this.state.category}
                                current_items={this.state.menu_dict[this.state.category] || []}
                                category_lst={this.state.category_lst}
                                menu_dict={this.state.menu_dict}
                                nutrition_dict={this.state.nutrition_dict} 
                                selected_item={this.state.selected_item}
                                selected_item_idx={this.state.selected_item_idx}
                                selected_item_lst={this.state.selected_item_lst}

                                // CategoryMenu
                                onCategoryMenuChange={this.handleCategoryMenuChange}
                                // MenuItems
                                onDeleteItem={this.handleDeleteItem}
                                onSubmitNewItem={this.handleSubmitNewItem}
                                // AddButton & DropButton
                                onUpdateSelected={this.handleUpdateSelected}
                                // SelectedItems
                                onChangeSelect={this.handleChangeSelect}/> 
                    </Col>
                </Row>
                <Row className="progress-div">
                    <Col  xxl={{offset: 0, size: 12}} xl={{offset: 0, size: 12}}  lg={{offset: 0, size: 12}} 
                md={{offset: 0, size: 12}} sm={{offset: 0, size: 12}} xs={{offset: 1, size: 10}}>
                        <ProgressBar 
                                key={this.state.selected_item_lst}
                                nutrition_dict={this.state.nutrition_dict}
                                selected_item_lst={this.state.selected_item_lst}
                                calorie_goal={this.state.calorie_goal}

                                onChangeGoal={this.handleChangeGoal}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <FoodLabels 
                                nutrition_dict={this.state.nutrition_dict}
                                selected_item={this.state.selected_item}
                                selected_item_lst={this.state.selected_item_lst} 

                                // SingleFoodLabel
                                onSubmitItem={this.handleSubmitItem}/> 
                    </Col>
                </Row>
            </Container>
        );
    }
}
export default FoodPlannerTable;
