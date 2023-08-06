/*! For license information please see a6962c3f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[38722,58261,8448,48191,32639,74844,73792],{14166:(t,e,i)=>{i.d(e,{W:()=>a});var n=function(){return n=Object.assign||function(t){for(var e,i=1,n=arguments.length;i<n;i++)for(var a in e=arguments[i])Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a]);return t},n.apply(this,arguments)};function a(t,e,i){void 0===e&&(e=Date.now()),void 0===i&&(i={});var a=n(n({},o),i||{}),s=(+t-+e)/1e3;if(Math.abs(s)<a.second)return{value:Math.round(s),unit:"second"};var r=s/60;if(Math.abs(r)<a.minute)return{value:Math.round(r),unit:"minute"};var l=s/3600;if(Math.abs(l)<a.hour)return{value:Math.round(l),unit:"hour"};var p=s/86400;if(Math.abs(p)<a.day)return{value:Math.round(p),unit:"day"};var h=new Date(t),u=new Date(e),d=h.getFullYear()-u.getFullYear();if(Math.round(Math.abs(d))>0)return{value:Math.round(d),unit:"year"};var c=12*d+h.getMonth()-u.getMonth();if(Math.round(Math.abs(c))>0)return{value:Math.round(c),unit:"month"};var m=s/604800;return{value:Math.round(m),unit:"week"}}var o={second:45,minute:45,hour:22,day:5}},18601:(t,e,i)=>{i.d(e,{qN:()=>r.q,Wg:()=>p});var n,a,o=i(87480),s=i(72367),r=i(78220);const l=null!==(a=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==a&&a;class p extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,o.__decorate)([(0,s.Cb)({type:Boolean})],p.prototype,"disabled",void 0)},15112:(t,e,i)=>{i.d(e,{P:()=>a});i(94604);var n=i(9672);class a{constructor(t){a[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return a.types[t]&&a.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=a.types[e]=a.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=a.types[this.type];return t?Object.keys(t).map((function(t){return o[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}a[" "]=function(){},a.types={};var o=a.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new a({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new a({type:this.type,key:t}).value}})},54444:(t,e,i)=>{i(94604);var n=i(9672),a=i(87156),o=i(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,a.vz)(this).parentNode,e=(0,a.vz)(this).getOwnerRoot();return this.for?(0,a.vz)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,a.vz)(this).textContent.trim()){for(var t=!0,e=(0,a.vz)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,n=this.offsetParent.getBoundingClientRect(),a=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(a.width-o.width)/2,r=(a.height-o.height)/2,l=a.left-n.left,p=a.top-n.top;switch(this.position){case"top":e=l+s,i=p-o.height-t;break;case"bottom":e=l+s,i=p+a.height+t;break;case"left":e=l-o.width-t,i=p+r;break;case"right":e=l+a.width+t,i=p+r}this.fitToVisibleBounds?(n.left+e+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),n.top+i+o.height>window.innerHeight?(this.style.bottom=n.height-p+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,e,i)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var e={};return Object.keys(t).forEach((function(i){e[i]=n(t[i])})),e}i.d(e,{Z:()=>n})},93217:(t,e,i)=>{i.d(e,{Ud:()=>u});const n=Symbol("Comlink.proxy"),a=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.thrown"),r=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>r(t)&&t[n],serialize(t){const{port1:e,port2:i}=new MessageChannel;return p(t,e),[i,[i]]},deserialize:t=>(t.start(),u(t))}],["throw",{canHandle:t=>r(t)&&s in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function p(t,e=self){e.addEventListener("message",(function i(a){if(!a||!a.data)return;const{id:o,type:r,path:l}=Object.assign({path:[]},a.data),u=(a.data.argumentList||[]).map(v);let d;try{const e=l.slice(0,-1).reduce(((t,e)=>t[e]),t),i=l.reduce(((t,e)=>t[e]),t);switch(r){case"GET":d=i;break;case"SET":e[l.slice(-1)[0]]=v(a.data.value),d=!0;break;case"APPLY":d=i.apply(e,u);break;case"CONSTRUCT":d=function(t){return Object.assign(t,{[n]:!0})}(new i(...u));break;case"ENDPOINT":{const{port1:e,port2:i}=new MessageChannel;p(t,i),d=function(t,e){return f.set(t,e),t}(e,[e])}break;case"RELEASE":d=void 0;break;default:return}}catch(t){d={value:t,[s]:0}}Promise.resolve(d).catch((t=>({value:t,[s]:0}))).then((t=>{const[n,a]=y(t);e.postMessage(Object.assign(Object.assign({},n),{id:o}),a),"RELEASE"===r&&(e.removeEventListener("message",i),h(e))}))})),e.start&&e.start()}function h(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function u(t,e){return c(t,[],e)}function d(t){if(t)throw new Error("Proxy has been released and is not useable")}function c(t,e=[],i=function(){}){let n=!1;const s=new Proxy(i,{get(i,a){if(d(n),a===o)return()=>g(t,{type:"RELEASE",path:e.map((t=>t.toString()))}).then((()=>{h(t),n=!0}));if("then"===a){if(0===e.length)return{then:()=>s};const i=g(t,{type:"GET",path:e.map((t=>t.toString()))}).then(v);return i.then.bind(i)}return c(t,[...e,a])},set(i,a,o){d(n);const[s,r]=y(o);return g(t,{type:"SET",path:[...e,a].map((t=>t.toString())),value:s},r).then(v)},apply(i,o,s){d(n);const r=e[e.length-1];if(r===a)return g(t,{type:"ENDPOINT"}).then(v);if("bind"===r)return c(t,e.slice(0,-1));const[l,p]=m(s);return g(t,{type:"APPLY",path:e.map((t=>t.toString())),argumentList:l},p).then(v)},construct(i,a){d(n);const[o,s]=m(a);return g(t,{type:"CONSTRUCT",path:e.map((t=>t.toString())),argumentList:o},s).then(v)}});return s}function m(t){const e=t.map(y);return[e.map((t=>t[0])),(i=e.map((t=>t[1])),Array.prototype.concat.apply([],i))];var i}const f=new WeakMap;function y(t){for(const[e,i]of l)if(i.canHandle(t)){const[n,a]=i.serialize(t);return[{type:"HANDLER",name:e,value:n},a]}return[{type:"RAW",value:t},f.get(t)||[]]}function v(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function g(t,e,i){return new Promise((n=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(i){i.data&&i.data.id&&i.data.id===a&&(t.removeEventListener("message",e),n(i.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:a},e),i)}))}},19596:(t,e,i)=>{i.d(e,{s:()=>u});var n=i(81563),a=i(38941);const o=(t,e)=>{var i,n;const a=t._$AN;if(void 0===a)return!1;for(const t of a)null===(n=(i=t)._$AO)||void 0===n||n.call(i,e,!1),o(t,e);return!0},s=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},r=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),h(e)}};function l(t){void 0!==this._$AN?(s(this),this._$AM=t,r(this)):this._$AM=t}function p(t,e=!1,i=0){const n=this._$AH,a=this._$AN;if(void 0!==a&&0!==a.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)o(n[t],!1),s(n[t]);else null!=n&&(o(n,!1),s(n));else o(this,t)}const h=t=>{var e,i,n,o;t.type==a.pX.CHILD&&(null!==(e=(n=t)._$AP)&&void 0!==e||(n._$AP=p),null!==(i=(o=t)._$AQ)&&void 0!==i||(o._$AQ=l))};class u extends a.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),r(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,n;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),e&&(o(this,t),s(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}},81563:(t,e,i)=>{i.d(e,{E_:()=>f,i9:()=>c,_Y:()=>p,pt:()=>o,OR:()=>r,hN:()=>s,ws:()=>m,fk:()=>h,hl:()=>d});var n=i(15304);const{H:a}=n.Al,o=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,e)=>{var i,n;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(n=t)||void 0===n?void 0:n._$litType$)===e},r=t=>void 0===t.strings,l=()=>document.createComment(""),p=(t,e,i)=>{var n;const o=t._$AA.parentNode,s=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=o.insertBefore(l(),s),n=o.insertBefore(l(),s);i=new a(e,n,t,t.options)}else{const e=i._$AB.nextSibling,a=i._$AM,r=a!==t;if(r){let e;null===(n=i._$AQ)||void 0===n||n.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==a._$AU&&i._$AP(e)}if(e!==s||r){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;o.insertBefore(t,s),t=e}}}return i},h=(t,e,i=t)=>(t._$AI(e,i),t),u={},d=(t,e=u)=>t._$AH=e,c=t=>t._$AH,m=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const n=t._$AB.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},f=t=>{t._$AR()}},57835:(t,e,i)=>{i.d(e,{Xe:()=>n.Xe,pX:()=>n.pX,XM:()=>n.XM});var n=i(38941)}}]);
//# sourceMappingURL=a6962c3f.js.map