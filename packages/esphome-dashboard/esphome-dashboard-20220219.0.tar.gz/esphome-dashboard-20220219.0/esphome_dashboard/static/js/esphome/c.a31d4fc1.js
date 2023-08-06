import{r as o,_ as t,c as e,f as i,n as r,s as a,$ as s}from"./index-7481a400.js";import"./c.350632ad.js";import{a as n}from"./c.31a5ce83.js";import{g as c}from"./c.ebe42031.js";import"./c.005c9341.js";import"./c.a25cfa1d.js";import"./c.c1911bb5.js";import"./c.515f4acf.js";let d=class extends a{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return s`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?s`
              <a
                slot="secondaryAction"
                href="${c(this.configuration,this.downloadFactoryFirmware)}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:s`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const t=document.createElement("a");t.download=this.configuration+".bin",t.href=c(this.configuration,this.downloadFactoryFirmware),document.body.appendChild(t),t.click(),t.remove()}_handleRetry(){n(this.configuration,this.downloadFactoryFirmware)}_handleClose(){this.parentNode.removeChild(this)}};d.styles=o`
    a {
      text-decoration: none;
    }
  `,t([e()],d.prototype,"configuration",void 0),t([e()],d.prototype,"downloadFactoryFirmware",void 0),t([i()],d.prototype,"_result",void 0),d=t([r("esphome-compile-dialog")],d);
