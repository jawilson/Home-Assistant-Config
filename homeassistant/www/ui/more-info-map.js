import {
  LitElement, html
} from 'https://unpkg.com/@polymer/lit-element@^0.5.2/lit-element.js?module';

class MoreInfoMap extends LitElement {
  static get properties() {
    return {
      hass: Object,
      stateObj: Object,
    }
  }

  _render({hass, stateObj}) {
    var src;
    if (stateObj && 'latitude' in stateObj.attributes) {
      var entity_id = stateObj.attributes.entity_id;
      var entity = entity_id.split('.')[1]; 
      src = hass.states['camera.' + entity].attributes.entity_picture
    }
    else {
      src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }

    var keys = ['source_type', 'gps_accuracy', 'location_type'];
    var attributes = keys.reduce(function(attributes, key) {
      if (key in stateObj.attributes) {
        var attribute = document.createElement('div');
        attribute.className = "data-entry layout justified horizontal";

        var keyNode = document.createElement('div');
        keyNode.className = "key"
        keyNode.appendChild(document.createTextNode(key.replace('_', ' ')));

        var valueNode = document.createElement('div');
        valueNode.className = "value";
        valueNode.appendChild(document.createTextNode(stateObj.attributes[key]));

        attribute.appendChild(keyNode);
        attribute.appendChild(valueNode);
        attributes.appendChild(attribute);
      }

      return attributes;
    }, document.createElement('div'));
    attributes.className = "layout vertical";

    // Return an empty image if no stateObj (= dialog not open) or in cleanup mode.
    return html`
      <style>
        :host {
          max-width:640px;
        }

        .map-image {
          width: 100%;
        }

        .layout.horizontal, .layout.vertical {
          display: -ms-flexbox;
                display: -webkit-flex;
                display: flex;
        }

        .layout.horizontal {
          -ms-flex-direction: row;
                -webkit-flex-direction: row;
                flex-direction: row;
        }

        .layout.vertical {
          -ms-flex-direction: column;
                -webkit-flex-direction: column;
                flex-direction: column;
        }

        .layout.justified {
          -ms-flex-pack: justify;
                -webkit-justify-content: space-between;
                justify-content: space-between;
        }

        .data-entry .value {
          max-width: 200px;
        }
      </style>
      <img class="map-image" @on-load=${(e) => this.imageLoaded()} src="${src}"/>
      ${attributes}
    `;
  }

  imageLoaded() {
    console.log('image loaded');
    this.dispatchEvent(new Event('iron-resize', {bubbles: true, composed: true}));
  }
}
customElements.define('more-info-map', MoreInfoMap);
