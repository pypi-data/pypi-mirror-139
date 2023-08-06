import{_ as o,c as t,f as s,n as e,s as i,$ as a,Q as r}from"./index-7481a400.js";import"./c.350632ad.js";import{o as c}from"./c.289c8792.js";import"./c.005c9341.js";import"./c.a25cfa1d.js";import"./c.515f4acf.js";let n=class extends i{render(){return a`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){r(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],n.prototype,"configuration",void 0),o([t()],n.prototype,"target",void 0),o([s()],n.prototype,"_result",void 0),n=o([e("esphome-logs-dialog")],n);
