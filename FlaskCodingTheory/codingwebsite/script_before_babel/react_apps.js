'use strict';

const e = React.createElement;


class BitButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
     };
     this.onClick = this.onClick.bind(this)
  }

  onClick(event) {
    this.props.handleBitClicked(this.props.uniqueID, this.props.bit, this.props.changed)    
  }

  render() {
    if (this.props.changed) {
      return (
      <button className="btn btn-danger ml-1" onClick={this.onClick}>
      {this.props.bit}
      </button>
      );
    }

    return (
      <button className="btn btn-light ml-1" onClick={this.onClick}>
      {this.props.bit}
      </button>
      );
  }
}


class EncodeRow extends React.Component{
  constructor(props){
    super(props);
    this.state={
    value: ""
    };
    this.handleChange = this.handleChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit(event){
    this.props.handleSubmit(this.state.value)
  }

  onlyContainsFrom(text, allowedCharacters){
    for(let i = 0; i < text.length; i++){
      if(!allowedCharacters.includes(text.charAt(i))){
        return false;
      }
    }
    return true;
  }

  handleChange(event){
    if(!this.props.allowedCharacters || this.onlyContainsFrom(event.target.value, this.props.allowedCharacters)){
      this.setState({value: event.target.value})
    }
  }


  render() {
    return (<form onSubmit={this.onSubmit}>
                  <fieldset className="form-group">
                     <div className="form-group">
                        <p className="lead">Message:</p>
                        <input type="text" dir="auto" value={this.state.value} onChange={this.handleChange} className = "form-control" 
                        style={{backgroundColor:"#272727", color:"white"}}/>
                     </div>
                     <div className="form-group">
                        <input type="submit" value="Encode" className="btn btn-dark btn-lg"/>
                     </div>
                  </fieldset>
               </form>);
  }

}
class DecodeRow extends React.Component{
  constructor(props){
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit(event){
    this.props.handleSubmit(event.target.value);
  }

  handleChange(event){
    this.props.superHandleChange(event.target.value);
  }


  render() {
    return (<form onSubmit={this.onSubmit}>
                  <fieldset className="form-group">
                     <div className="form-group">
                        <p className="lead">{this.props.heading}</p>
                        <input type="text" dir="auto" value={this.props.encodedText} onChange={this.handleChange} className = "form-control" 
                        style={{backgroundColor:"#272727", color:"white"}}/>
                     </div>
                     <div className="form-group">
                        <input type="submit" value="Decode" className="btn btn-dark btn-lg"/>
                     </div>
                  </fieldset>
               </form>);
  }

}
class HammingCodeApp extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      encodedText:'',
      decoded:''
    }

    this.uniqueValue = 0;
    this.handleEncode = this.handleEncode.bind(this);
    this.handleDecode = this.handleDecode.bind(this);
    this.handleDecodeChange = this.handleDecodeChange.bind(this);
    //this.handleBitClicked = this.handleBitClicked.bind(this);
    /*this.getEncodedStringFromButtons = this.getEncodedStringFromButtons.bind(this);*/
  }

  /*getEncodedStringFromButtons(){
    let encodedString = this.state.bitButtons.reduce((encodedString, bitButton)=> 
      encodedString.concat(bitButton.props.bit.toString())
    , "");
    
    return encodedString;
  }*/
  /*handleBitClicked(uniqueID, bit, changed){
    const newChanged = !changed;
    let newBit = 2;
    if (bit == 0){
      newBit = 1;
    }else{
      newBit = 0;
    }
    let newBitButtons = []
    this.state.bitButtons.forEach(bitButton => {
      if(bitButton.props.uniqueID == uniqueID){
        this.uniqueValue = this.uniqueValue + 1;
        newBitButtons.push(<BitButton key = {this.uniqueValue} uniqueID={this.uniqueValue} bit = {newBit} changed = {newChanged} handleBitClicked = {this.handleBitClicked} />);
      }else{
        newBitButtons.push(bitButton);
      }
    });
    this.setState({bitButtons:newBitButtons})
  }*/

  convertBitsToDNA(bits){
    let dnaString = ""
    for(let i = 0; i < bits.length; i++){
      if(bits.charAt(i) == 0){
        if(Math.floor(Math.random() * 2)){
          dnaString += "T"
        }else{
          dnaString += "A"
        }
      }else if(bits.charAt(i) == 1){
        if(Math.floor(Math.random() * 2)){
          dnaString += "C"
        }else{
          dnaString += "G"
        }
      }
    }
    return dnaString;
  }

  convertDNAToBits(dna){
    let bitString = ""
    for(let i = 0; i < dna.length; i++){
      if(dna.charAt(i) == "T" || dna.charAt(i) == "A"){
        bitString += "0"
      }else if(dna.charAt(i) == "C" || dna.charAt(i) == "G"){
        bitString += "1"
      }
    }
    return bitString;
  }

  onlyContainsFrom(text, allowedCharacters){
    for(let i = 0; i < text.length; i++){
      if(!allowedCharacters.includes(text.charAt(i))){
        return false;
      }
    }
    return true;
  }
  handleDecodeChange(value){
    if(this.onlyContainsFrom(value, "TACGtacg")){
      this.setState({encodedText:value.toUpperCase()})
    }
  }
  handleEncode(value){
    event.preventDefault();

    let verifiedValue = value;

    var xhr = new XMLHttpRequest();

    
    // open the request with the verb and the url
    xhr.open('GET', 'http://localhost:5000/hammingCode?message=' + verifiedValue);
    // get a callback when the server responds
    xhr.addEventListener('load', () => {
      // update the state of the component with the result here
    let bits = JSON.parse(xhr.responseText)["code"];

      //this.setState({bitRowTitle: "Encoded Bits (click to change):", bitRowBits:bits})
    /*let bitButtons = Array.from(bits).map(
      bit => {
        this.uniqueValue = this.uniqueValue + 1
        return <BitButton key = {this.uniqueValue} uniqueID={this.uniqueValue} bit = {bit} changed = {false} handleBitClicked = {this.handleBitClicked} />;
        }
      );*/

    
    this.setState({encodedText:this.convertBitsToDNA(bits)})
    })

    // send the request
    xhr.send()
  }

  handleDecode(value){
    event.preventDefault()
    var xhr = new XMLHttpRequest();
    let code = this.convertDNAToBits(this.state.encodedText);
    
    // open the request with the verb and the url
    xhr.open('GET', 'http://localhost:5000/hammingDecode?code=' + code);
    // get a callback when the server responds
    xhr.addEventListener('load', () => {
      // update the state of the component with the result here
      let message = JSON.parse(xhr.responseText)["message"];
      //console.log(bits)
      //console.log(xhr.responseText)
      this.setState({decoded:message}) 
      
    })

    // send the request
    xhr.send()
  }

  componentDidUpdate(){
     document.querySelector('.hamming-popover') != null && $(document).ready(function(){ $('.hamming-popover').popover()}); 
  }
  render(){
   return (<div className="container">
               <EncodeRow handleSubmit={this.handleEncode} />
                <DecodeRow handleSubmit={this.handleDecode} superHandleChange = {this.handleDecodeChange} heading = "DNA Hamming Code:" encodedText = {this.state.encodedText}/>
                {this.state.encodeRow && 
                <button type="button" className="hamming-popover btn btn-outline-light btn-sm" data-toggle="popover" style={{fontSize:"15px"}} title="Click to introduce errors" data-content="Hamming Codes can correct 1 error and detect upto 2 errors. If 3 or more errors occur, Hamming Codes are incorrectly decoded.">?</button>}
                <div className="form-group mt-4">
                  
               </div>
               <div className="mt-4">
                  <p className="lead">{this.state.decoded.length != 0 && "Decoded Bits:"}</p>
                  <p className="lead" style={{fontWeight:"300"}}>{this.state.decoded}</p>
               </div>
                              
            </div>
          )
  }
}



//Rendering

ReactDOM.render(<HammingCodeApp />, document.querySelector(".hamming_app_container"))