import{_ as e,c as t,n as o,s as i,$ as a,P as l}from"./index-7481a400.js";import"./c.005c9341.js";import{d as n}from"./c.ebe42031.js";let s=class extends i{render(){return a`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await n(this.configuration),l(this,"deleted")}};e([t()],s.prototype,"name",void 0),e([t()],s.prototype,"configuration",void 0),s=e([o("esphome-delete-device-dialog")],s);
