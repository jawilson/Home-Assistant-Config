function getEntities(hass, entities) {
  return entities.filter((entity) => {
    const stateObj = hass.states[entity];
    return stateObj && stateObj.attributes.hidden !== true;
  });
}

class EntitiesCard extends HTMLElement {
  getCardSize() {
    return this.lastChild ? this.lastChild.getCardSize() : 1;
  }

  setConfig(config) {
    this._config = config;
    this._configEntities = config.entities;

    if (this.lastChild) {
      this.removeChild(this.lastChild);
      this._element = null;
    }

    const card = 'card' in config ? Object.assign({}, config.card) : {}
    if (!card.type) card.type = 'entities';
    card.entities = [];

    const element = document.createElement(`hui-${card.type}-card`);
    element._filterRawConfig = card;
    this.appendChild(element);

    this._element = element;
  }

  set hass(hass) {
    const element = this._element;
    if (!element || element.tagName === 'HUI-ERROR-CARD' || !hass) return;
    const entitiesList = getEntities(hass, this._configEntities);

    if (entitiesList.length === 0 && this._config.show_empty === false) {
      this.style.display = 'none';
      return;
    }

    this.style.display = 'block';
    element.setConfig(Object.assign(
      {},
      element._filterRawConfig,
      { entities: entitiesList }
    ));
    element.isPanel = this.isPanel;
    element.hass = hass;

    // Attach element if it has never been attached.
    if (!this.lastChild) this.appendChild(element);
  }

}
customElements.define('entity-hidden-filter-card', EntitiesCard);
