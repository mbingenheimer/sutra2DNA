'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var e = React.createElement;

var BitButton = function (_React$Component) {
  _inherits(BitButton, _React$Component);

  function BitButton(props) {
    _classCallCheck(this, BitButton);

    var _this = _possibleConstructorReturn(this, (BitButton.__proto__ || Object.getPrototypeOf(BitButton)).call(this, props));

    _this.state = {};
    _this.onClick = _this.onClick.bind(_this);
    return _this;
  }

  _createClass(BitButton, [{
    key: "onClick",
    value: function onClick(event) {
      this.props.handleBitClicked(this.props.uniqueID, this.props.bit, this.props.changed);
    }
  }, {
    key: "render",
    value: function render() {
      if (this.props.changed) {
        return React.createElement(
          "button",
          { className: "btn btn-danger ml-1", onClick: this.onClick },
          this.props.bit
        );
      }

      return React.createElement(
        "button",
        { className: "btn btn-light ml-1", onClick: this.onClick },
        this.props.bit
      );
    }
  }]);

  return BitButton;
}(React.Component);

var Helpers = function () {
  function Helpers() {
    _classCallCheck(this, Helpers);
  }

  _createClass(Helpers, null, [{
    key: "convertBitsToDNA",
    value: function convertBitsToDNA(bits) {
      var dnaString = "";
      for (var i = 0; i < bits.length; i++) {
        if (bits.charAt(i) == 0) {
          if (Math.floor(Math.random() * 2)) {
            dnaString += "T";
          } else {
            dnaString += "A";
          }
        } else if (bits.charAt(i) == 1) {
          if (Math.floor(Math.random() * 2)) {
            dnaString += "C";
          } else {
            dnaString += "G";
          }
        }
      }
      return dnaString;
    }
  }, {
    key: "convertDNAToBits",
    value: function convertDNAToBits(dna) {
      var bitString = "";
      for (var i = 0; i < dna.length; i++) {
        if (dna.charAt(i) == "T" || dna.charAt(i) == "A") {
          bitString += "0";
        } else if (dna.charAt(i) == "C" || dna.charAt(i) == "G") {
          bitString += "1";
        }
      }
      return bitString;
    }
  }, {
    key: "onlyContainsFrom",
    value: function onlyContainsFrom(text, allowedCharacters) {
      for (var i = 0; i < text.length; i++) {
        if (!allowedCharacters.includes(text.charAt(i))) {
          return false;
        }
      }
      return true;
    }
  }]);

  return Helpers;
}();

var EncodeRow = function (_React$Component2) {
  _inherits(EncodeRow, _React$Component2);

  function EncodeRow(props) {
    _classCallCheck(this, EncodeRow);

    var _this2 = _possibleConstructorReturn(this, (EncodeRow.__proto__ || Object.getPrototypeOf(EncodeRow)).call(this, props));

    _this2.state = {
      value: ""
    };
    _this2.handleChange = _this2.handleChange.bind(_this2);
    _this2.onSubmit = _this2.onSubmit.bind(_this2);
    return _this2;
  }

  _createClass(EncodeRow, [{
    key: "onSubmit",
    value: function onSubmit(event) {
      this.props.handleSubmit(this.state.value);
    }
  }, {
    key: "handleChange",
    value: function handleChange(event) {
      if (!this.props.allowedCharacters || Helpers.onlyContainsFrom(event.target.value, this.props.allowedCharacters)) {
        this.setState({ value: event.target.value });
      }
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(
        "form",
        { onSubmit: this.onSubmit },
        React.createElement(
          "fieldset",
          { className: "form-group" },
          React.createElement(
            "div",
            { className: "form-group" },
            React.createElement(
              "p",
              { className: "lead" },
              "Message:"
            ),
            React.createElement("input", { type: "text", dir: "auto", value: this.state.value, onChange: this.handleChange, className: "form-control",
              style: { backgroundColor: "#272727", color: "white" } })
          ),
          React.createElement(
            "div",
            { className: "form-group" },
            React.createElement("input", { type: "submit", value: "Encode", className: "btn btn-dark btn-lg" })
          )
        )
      );
    }
  }]);

  return EncodeRow;
}(React.Component);

var DecodeRow = function (_React$Component3) {
  _inherits(DecodeRow, _React$Component3);

  function DecodeRow(props) {
    _classCallCheck(this, DecodeRow);

    var _this3 = _possibleConstructorReturn(this, (DecodeRow.__proto__ || Object.getPrototypeOf(DecodeRow)).call(this, props));

    _this3.handleChange = _this3.handleChange.bind(_this3);
    _this3.onSubmit = _this3.onSubmit.bind(_this3);
    return _this3;
  }

  _createClass(DecodeRow, [{
    key: "onSubmit",
    value: function onSubmit(event) {
      this.props.handleSubmit(event.target.value);
    }
  }, {
    key: "handleChange",
    value: function handleChange(event) {
      this.props.superHandleChange(event.target.value);
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(
        "form",
        { onSubmit: this.onSubmit },
        React.createElement(
          "fieldset",
          { className: "form-group" },
          React.createElement(
            "div",
            { className: "form-group" },
            React.createElement(
              "p",
              { className: "lead" },
              this.props.heading
            ),
            React.createElement("input", { type: "text", dir: "auto", value: this.props.encodedText, onChange: this.handleChange, className: "form-control",
              style: { backgroundColor: "#272727", color: "white" } })
          ),
          React.createElement(
            "div",
            { className: "form-group" },
            React.createElement("input", { type: "submit", value: "Decode", className: "btn btn-dark btn-lg" })
          )
        )
      );
    }
  }]);

  return DecodeRow;
}(React.Component);

var HammingCodeApp = function (_React$Component4) {
  _inherits(HammingCodeApp, _React$Component4);

  function HammingCodeApp(props) {
    _classCallCheck(this, HammingCodeApp);

    var _this4 = _possibleConstructorReturn(this, (HammingCodeApp.__proto__ || Object.getPrototypeOf(HammingCodeApp)).call(this, props));

    _this4.state = {
      encodedText: '',
      decoded: ''
    };

    _this4.uniqueValue = 0;
    _this4.handleEncode = _this4.handleEncode.bind(_this4);
    _this4.handleDecode = _this4.handleDecode.bind(_this4);
    _this4.handleDecodeChange = _this4.handleDecodeChange.bind(_this4);
    //this.handleBitClicked = this.handleBitClicked.bind(this);
    /*this.getEncodedStringFromButtons = this.getEncodedStringFromButtons.bind(this);*/
    return _this4;
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

  _createClass(HammingCodeApp, [{
    key: "handleDecodeChange",
    value: function handleDecodeChange(value) {
      if (Helpers.onlyContainsFrom(value, "TACGtacg")) {
        this.setState({ encodedText: value.toUpperCase() });
      }
    }
  }, {
    key: "handleEncode",
    value: function handleEncode(value) {
      var _this5 = this;

      event.preventDefault();

      var verifiedValue = value;

      var xhr = new XMLHttpRequest();

      // open the request with the verb and the url
      xhr.open('GET', 'http://localhost:5000/hammingCode?message=' + verifiedValue);
      // get a callback when the server responds
      xhr.addEventListener('load', function () {
        // update the state of the component with the result here
        var bits = JSON.parse(xhr.responseText)["code"];

        //this.setState({bitRowTitle: "Encoded Bits (click to change):", bitRowBits:bits})
        /*let bitButtons = Array.from(bits).map(
          bit => {
            this.uniqueValue = this.uniqueValue + 1
            return <BitButton key = {this.uniqueValue} uniqueID={this.uniqueValue} bit = {bit} changed = {false} handleBitClicked = {this.handleBitClicked} />;
            }
          );*/

        _this5.setState({ encodedText: Helpers.convertBitsToDNA(bits) });
      });

      // send the request
      xhr.send();
    }
  }, {
    key: "handleDecode",
    value: function handleDecode(value) {
      var _this6 = this;

      event.preventDefault();
      var xhr = new XMLHttpRequest();
      var code = Helpers.convertDNAToBits(this.state.encodedText);

      // open the request with the verb and the url
      xhr.open('GET', 'http://localhost:5000/hammingDecode?code=' + code);
      // get a callback when the server responds
      xhr.addEventListener('load', function () {
        // update the state of the component with the result here
        var message = JSON.parse(xhr.responseText)["message"];
        //console.log(bits)
        //console.log(xhr.responseText)
        _this6.setState({ decoded: message });
      });

      // send the request
      xhr.send();
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate() {
      document.querySelector('.hamming-popover') != null && $(document).ready(function () {
        $('.hamming-popover').popover();
      });
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(
        "div",
        { className: "container" },
        React.createElement(EncodeRow, { handleSubmit: this.handleEncode }),
        React.createElement(DecodeRow, { handleSubmit: this.handleDecode, superHandleChange: this.handleDecodeChange, heading: "DNA Hamming Code:", encodedText: this.state.encodedText }),
        this.state.encodeRow && React.createElement(
          "button",
          { type: "button", className: "hamming-popover btn btn-outline-light btn-sm", "data-toggle": "popover", style: { fontSize: "15px" }, title: "Click to introduce errors", "data-content": "Hamming Codes can correct 1 error and detect upto 2 errors. If 3 or more errors occur, Hamming Codes are incorrectly decoded." },
          "?"
        ),
        React.createElement("div", { className: "form-group mt-4" }),
        React.createElement(
          "div",
          { className: "mt-4" },
          React.createElement(
            "p",
            { className: "lead" },
            this.state.decoded.length != 0 && "Decoded Message:"
          ),
          React.createElement(
            "p",
            { className: "lead", style: { fontWeight: "300" } },
            this.state.decoded
          )
        )
      );
    }
  }]);

  return HammingCodeApp;
}(React.Component);

//Rendering Hamming Code App

if (document.querySelector(".hamming_app_container")) {
  ReactDOM.render(React.createElement(HammingCodeApp, null), document.querySelector(".hamming_app_container"));
}

// Reed-Solomon App Code Start


var ReedSolomonCodeApp = function (_React$Component5) {
  _inherits(ReedSolomonCodeApp, _React$Component5);

  function ReedSolomonCodeApp(props) {
    _classCallCheck(this, ReedSolomonCodeApp);

    var _this7 = _possibleConstructorReturn(this, (ReedSolomonCodeApp.__proto__ || Object.getPrototypeOf(ReedSolomonCodeApp)).call(this, props));

    _this7.state = {
      encodedText: '',
      decoded: '',
      noErrors: 3
    };

    _this7.uniqueValue = 0;
    _this7.handleEncode = _this7.handleEncode.bind(_this7);
    _this7.handleDecode = _this7.handleDecode.bind(_this7);
    _this7.handleDecodeChange = _this7.handleDecodeChange.bind(_this7);
    _this7.handleErrorsChange = _this7.handleErrorsChange.bind(_this7);
    //this.handleBitClicked = this.handleBitClicked.bind(this);
    /*this.getEncodedStringFromButtons = this.getEncodedStringFromButtons.bind(this);*/
    return _this7;
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

  _createClass(ReedSolomonCodeApp, [{
    key: "handleErrorsChange",
    value: function handleErrorsChange(event) {
      if (event.target.value <= 5 && event.target.value >= 0) {
        this.setState({ noErrors: event.target.value });
      }
    }
  }, {
    key: "handleDecodeChange",
    value: function handleDecodeChange(value) {
      if (Helpers.onlyContainsFrom(value, "TACGtacg")) {
        this.setState({ encodedText: value.toUpperCase() });
      }
    }
  }, {
    key: "handleEncode",
    value: function handleEncode(value) {
      var _this8 = this;

      event.preventDefault();

      var verifiedValue = value;

      var xhr = new XMLHttpRequest();
      console.log("Here");

      // open the request with the verb and the url
      xhr.open('GET', 'http://localhost:5000/rsCode?message=' + verifiedValue + "&noErrors=" + (parseInt(this.state.noErrors) + 1).toString());
      // get a callback when the server responds
      xhr.addEventListener('load', function () {
        // update the state of the component with the result here
        var bits = JSON.parse(xhr.responseText)["code"];

        //this.setState({bitRowTitle: "Encoded Bits (click to change):", bitRowBits:bits})
        /*let bitButtons = Array.from(bits).map(
          bit => {
            this.uniqueValue = this.uniqueValue + 1
            return <BitButton key = {this.uniqueValue} uniqueID={this.uniqueValue} bit = {bit} changed = {false} handleBitClicked = {this.handleBitClicked} />;
            }
          );*/

        _this8.setState({ encodedText: Helpers.convertBitsToDNA(bits) });
      });

      // send the request
      xhr.send();
    }
  }, {
    key: "handleDecode",
    value: function handleDecode(value) {
      var _this9 = this;

      event.preventDefault();
      var xhr = new XMLHttpRequest();
      var code = Helpers.convertDNAToBits(this.state.encodedText);

      // open the request with the verb and the url
      xhr.open('GET', 'http://localhost:5000/rsDecode?code=' + code + "&noErrors=" + (parseInt(this.state.noErrors) + 1).toString() + "&messageLength=" + this.state.encodedText.length.toString());
      // get a callback when the server responds
      xhr.addEventListener('load', function () {
        // update the state of the component with the result here
        var message = JSON.parse(xhr.responseText)["message"];
        //console.log(bits)
        //console.log(xhr.responseText)
        _this9.setState({ decoded: message });
      });

      // send the request
      xhr.send();
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate() {
      document.querySelector('.hamming-popover') != null && $(document).ready(function () {
        $('.hamming-popover').popover();
      });
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(
        "div",
        { className: "container" },
        React.createElement(EncodeRow, { handleSubmit: this.handleEncode }),
        React.createElement(DecodeRow, { handleSubmit: this.handleDecode, superHandleChange: this.handleDecodeChange, heading: "DNA Reed-Solomon Code:", encodedText: this.state.encodedText }),
        this.state.encodeRow && React.createElement(
          "button",
          { type: "button", className: "hamming-popover btn btn-outline-light btn-sm", "data-toggle": "popover", style: { fontSize: "15px" }, title: "Click to introduce errors", "data-content": "Hamming Codes can correct 1 error and detect upto 2 errors. If 3 or more errors occur, Hamming Codes are incorrectly decoded." },
          "?"
        ),
        React.createElement(
          "div",
          { className: "col-3 mr-auto ml-auto" },
          React.createElement(
            "p",
            { className: "lead" },
            "Number of errors:"
          ),
          React.createElement("input", { type: "number", dir: "auto", className: "form-control",
            style: { backgroundColor: "#272727", color: "white" }, onChange: this.handleErrorsChange, value: this.state.noErrors })
        ),
        React.createElement(
          "div",
          { className: "mt-4" },
          React.createElement(
            "p",
            { className: "lead" },
            this.state.decoded.length != 0 && "Decoded Message:"
          ),
          React.createElement(
            "p",
            { className: "lead", style: { fontWeight: "300" } },
            this.state.decoded
          )
        )
      );
    }
  }]);

  return ReedSolomonCodeApp;
}(React.Component);

if (document.querySelector(".reedsolomon_app_container")) {
  ReactDOM.render(React.createElement(ReedSolomonCodeApp, null), document.querySelector(".reedsolomon_app_container"));
}