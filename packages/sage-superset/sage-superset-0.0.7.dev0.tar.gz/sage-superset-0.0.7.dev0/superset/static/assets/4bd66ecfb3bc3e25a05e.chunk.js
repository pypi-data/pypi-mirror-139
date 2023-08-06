"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4502],{27989:(e,t,a)=>{a.d(t,{Z:()=>h});var n=a(67294),o=a(51995),l=a(61988),i=a(35932),r=a(74069),s=a(82191),d=a(34858),c=a(11965);const p=o.iK.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,u=o.iK.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`,h=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:o,addDangerToast:h,onModelImport:m,show:g,onHide:b,passwordFields:v=[],setPasswordFields:y=(()=>{})})=>{const[f,Z]=(0,n.useState)(!0),[x,_]=(0,n.useState)({}),[C,w]=(0,n.useState)(!1),[N,$]=(0,n.useState)(!1),[S,E]=(0,n.useState)([]),[k,T]=(0,n.useState)(!1),A=()=>{E([]),y([]),_({}),w(!1),$(!1),T(!1)},{state:{alreadyExists:U,passwordsNeeded:O},importResource:L}=(0,d.PW)(e,t,(e=>{A(),h(e)}));(0,n.useEffect)((()=>{y(O),O.length>0&&T(!1)}),[O,y]),(0,n.useEffect)((()=>{w(U.length>0),U.length>0&&T(!1)}),[U,w]);return f&&g&&Z(!1),(0,c.tZ)(r.Z,{name:"model",className:"import-model-modal",disablePrimaryButton:0===S.length||C&&!N||k,onHandledPrimaryAction:()=>{var e;(null==(e=S[0])?void 0:e.originFileObj)instanceof File&&(T(!0),L(S[0].originFileObj,x,N).then((e=>{e&&(A(),m())})))},onHide:()=>{Z(!0),b(),A()},primaryButtonName:C?(0,l.t)("Overwrite"):(0,l.t)("Import"),primaryButtonType:C?"danger":"primary",width:"750px",show:g,title:(0,c.tZ)("h4",null,(0,l.t)("Import %s",t))},(0,c.tZ)(u,null,(0,c.tZ)(s.gq,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:S,onChange:e=>{E([{...e.file,status:"done"}])},onRemove:e=>(E(S.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{}},(0,c.tZ)(i.Z,{loading:k},"Select file"))),0===v.length?null:(0,c.tZ)(n.Fragment,null,(0,c.tZ)("h5",null,"Database passwords"),(0,c.tZ)(p,null,a),v.map((e=>(0,c.tZ)(u,{key:`password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},e,(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:x[e],onChange:t=>_({...x,[e]:t.target.value})}))))),C?(0,c.tZ)(n.Fragment,null,(0,c.tZ)(u,null,(0,c.tZ)("div",{className:"confirm-overwrite"},o),(0,c.tZ)("div",{className:"control-label"},(0,l.t)('Type "%s" to confirm',(0,l.t)("OVERWRITE"))),(0,c.tZ)("input",{id:"overwrite",type:"text",onChange:e=>{var t,a;const n=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";$(n.toUpperCase()===(0,l.t)("OVERWRITE"))}}))):null)}},95413:(e,t,a)=>{a.d(t,{Y:()=>o});var n=a(61988);const o={name:(0,n.t)("Data"),tabs:[{name:"Databases",label:(0,n.t)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:(0,n.t)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:(0,n.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,n.t)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},73246:(e,t,a)=>{a.r(t),a.d(t,{default:()=>lt});var n=a(61988),o=a(51995),l=a(31069),i=a(67294),r=a(38703),s=a(91877),d=a(93185),c=a(34858),p=a(40768),u=a(14114),h=a(20755),m=a(17198),g=a(58593),b=a(70163),v=a(98289),y=a(95413),f=a(27989),Z=a(32228),x=a(40637),_=a(82191),C=a(29487),w=a(74069),N=a(35932);function $(){return $=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(e[n]=a[n])}return e},$.apply(this,arguments)}const S={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},E=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"];function k(e,t){for(;e&&t--;)e=e.previousElementSibling;return e}const T={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},A=Object.keys(T);class U extends i.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas.parentNode.removeChild(this.canvas)}setState(e,t){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,t)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(S).forEach((t=>{e.style[t]=S[t]})),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);E.forEach((t=>{this.canvas.style[t]=e[t]}))}reflow(e){const t=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(t){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${t}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map((e=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("");const a=this.putEllipsis(this.calcIndexes()),n=a>-1,o={clamped:n,text:n?this.units.slice(0,a).join(""):e.text};this.setState(o,e.onReflow.bind(this,o))}calcIndexes(){const e=[0];let t=this.canvas.firstElementChild;if(!t)return e;let a=0,n=1,o=t.offsetTop;for(;(t=t.nextElementSibling)&&(t.offsetTop>o&&(n++,e.push(a),o=t.offsetTop),a++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const t=e[this.maxLine],a=this.units.slice(0,t),n=this.canvas.children[t].offsetTop;this.canvas.innerHTML=a.map(((e,t)=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const o=this.canvas.lastElementChild;let l=k(o,2);for(;l&&(o.offsetTop>n||o.offsetHeight>l.offsetHeight||o.offsetTop>l.offsetTop);)this.canvas.removeChild(l),l=k(o,2),a.pop();return a.length}isClamped(){return this.clamped}render(){const{text:e,clamped:t}=this.state,a=this.props,{component:n,ellipsis:o,trimRight:l,className:r}=a,s=function(e,t){if(null==e)return{};var a,n,o={},l=Object.keys(e);for(n=0;n<l.length;n++)a=l[n],t.indexOf(a)>=0||(o[a]=e[a]);return o}(a,["component","ellipsis","trimRight","className"]);return i.createElement(n,$({className:`LinesEllipsis ${t?"LinesEllipsis--clamped":""} ${r}`,ref:e=>this.target=e},function(e,t){if(!e||"object"!=typeof e)return e;const a={};return Object.keys(e).forEach((n=>{t.indexOf(n)>-1||(a[n]=e[n])})),a}(s,A)),t&&l?e.replace(/[\s\uFEFF\xA0]+$/,""):e,i.createElement("wbr",null),t&&i.createElement("span",{className:"LinesEllipsis-ellipsis"},o))}}U.defaultProps=T;const O=U;var L=a(11965);const M=(0,o.iK)(N.Z)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,q=o.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,P=o.iK.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,D=o.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`,R=(0,o.iK)((({icon:e,altText:t,buttonText:a,...n})=>(0,L.tZ)(M,n,(0,L.tZ)(q,null,e&&(0,L.tZ)("img",{src:e,alt:t}),!e&&(0,L.tZ)(b.Z.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})),(0,L.tZ)(D,null,(0,L.tZ)(P,null,(0,L.tZ)(O,{text:a,maxLine:"2",basedOn:"words",trimRight:!0}))))))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`;var I,z=a(8272),F=a(1483);!function(e){e.SQLALCHEMY_URI="sqlalchemy_form",e.DYNAMIC_FORM="dynamic_form"}(I||(I={}));var j=a(94184),H=a.n(j),B=a(49576),Q=a(43700),V=a(94670);const K=L.iv`
  margin-bottom: 0;
`,Y=o.iK.header`
  border-bottom: ${({theme:e})=>`${.25*e.gridUnit}px solid\n    ${e.colors.grayscale.light2};`}
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-weight: bold;
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,J=L.iv`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,W=L.iv`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,G=e=>L.iv`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,X=e=>L.iv`
  padding-left: ${2*e.gridUnit}px;
`,ee=e=>L.iv`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,te=e=>L.iv`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-title > h4 {
    font-weight: bold;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,ae=e=>L.iv`
  border: 1px solid ${e.colors.info.base};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;

  .ant-alert-message {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }

  .ant-alert-description {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    a {
      text-decoration: underline;
    }

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,ne=o.iK.div`
  margin: 0 ${({theme:e})=>4*e.gridUnit}px -${({theme:e})=>4*e.gridUnit}px;
`,oe=e=>L.iv`
  border: ${e.colors.error.base} 1px solid;
  padding: ${4*e.gridUnit}px;
  margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;
  color: ${e.colors.error.dark2};
  .ant-alert-message {
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }
  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;
    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,le=e=>L.iv`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    text-align: left;
  }
`,ie=e=>L.iv`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
        margin-bottom: ${10*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 475px;
  }
`,re=e=>L.iv`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-bottom: 0;
  }
`,se=o.iK.div`
  margin-bottom: ${({theme:e})=>6*e.gridUnit}px;
  &.mb-0 {
    margin-bottom: 0;
  }
  &.mb-8 {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .input-container {
    display: flex;
    align-items: top;

    label {
      display: flex;
      margin-left: ${({theme:e})=>2*e.gridUnit}px;
      margin-top: ${({theme:e})=>.75*e.gridUnit}px;
      font-family: ${({theme:e})=>e.typography.families.sansSerif};
      font-size: ${({theme:e})=>e.typography.sizes.m}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>8*e.gridUnit}px;
    margin-bottom: 0;
    padding: 0;
    .control-label {
      margin-bottom: 0;
    }
    &.open {
      height: ${102}px;
      padding-right: ${({theme:e})=>5*e.gridUnit}px;
    }
  }
`,de=(0,o.iK)(V.Ad)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,ce=o.iK.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${255}px;
      &.ctas-open {
        height: ${357}px;
      }
    }
  }
`,pe=o.iK.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ue=e=>L.iv`
  font-weight: 400;
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,he=o.iK.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0px;
  }
`,me=(o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: bold;
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  text-transform: uppercase;
`),ge=o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: bold;
`,be=o.iK.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    text-transform: uppercase;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,ve=o.iK.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
      font-weight: bold;
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    text-transform: uppercase;
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,ye=(0,o.iK)(N.Z)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,fe=o.iK.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
`,Ze=o.iK.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
    font-weight: bold;
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-delete {
    align-self: center;
    background: ${({theme:e})=>e.colors.grayscale.light4};
    margin: 5px 5px 8px 5px;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,xe=({db:e,onInputChange:t,onTextChange:a,onEditorChange:o,onExtraInputChange:l,onExtraEditorChange:i})=>{var r,s,d,c,p,u,h,m,g,b,v;const y=!(null==e||!e.expose_in_sqllab),f=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas);return(0,L.tZ)(Q.Z,{expandIconPosition:"right",accordion:!0,css:e=>(e=>L.iv`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e)},(0,L.tZ)(Q.Z.Panel,{header:(0,L.tZ)("div",null,(0,L.tZ)("h4",null,"SQL Lab"),(0,L.tZ)("p",{className:"helper"},"Adjust how this database will interact with SQL Lab.")),key:"1"},(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:t,labelText:(0,n.t)("Expose database in SQL Lab")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Allow this database to be queried in SQL Lab")})),(0,L.tZ)(ce,{className:H()("expandable",{open:y,"ctas-open":f})},(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:t,labelText:(0,n.t)("Allow CREATE TABLE AS")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Allow creation of new tables based on queries")}))),(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:t,labelText:(0,n.t)("Allow CREATE VIEW AS")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Allow creation of new views based on queries")})),(0,L.tZ)(se,{className:H()("expandable",{open:f})},(0,L.tZ)("div",{className:"control-label"},(0,n.t)("CTAS & CVAS SCHEMA")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"text",name:"force_ctas_schema",value:(null==e?void 0:e.force_ctas_schema)||"",placeholder:(0,n.t)("Create or select schema..."),onChange:t})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")))),(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:t,labelText:(0,n.t)("Allow DML")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")}))),(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_multi_schema_metadata_fetch",indeterminate:!1,checked:!(null==e||!e.allow_multi_schema_metadata_fetch),onChange:t,labelText:(0,n.t)("Allow Multi Schema Metadata Fetch")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Allow SQL Lab to fetch a list of all tables and all views across all database schemas. For large data warehouse with thousands of tables, this can be expensive and put strain on the system.")}))),(0,L.tZ)(se,{css:K},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==e||null==(r=e.extra_json)||!r.cost_estimate_enabled),onChange:l,labelText:(0,n.t)("Enable query cost estimation")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("For Presto and Postgres, shows a button to compute cost before running a query.")}))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!(null==e||null==(s=e.extra_json)||!s.allows_virtual_table_explore),onChange:l,labelText:(0,n.t)("Allow this database to be explored")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})))))),(0,L.tZ)(Q.Z.Panel,{header:(0,L.tZ)("div",null,(0,L.tZ)("h4",null,"Performance"),(0,L.tZ)("p",{className:"helper"},"Adjust performance settings of this database.")),key:"2"},(0,L.tZ)(se,{className:"mb-8"},(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Chart cache timeout")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,n.t)("Enter duration in seconds"),onChange:t})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires. Note this defaults to the global timeout if undefined."))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Schema cache timeout")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"number",name:"schema_cache_timeout",value:(null==e||null==(d=e.extra_json)||null==(c=d.metadata_cache_timeout)?void 0:c.schema_cache_timeout)||"",placeholder:(0,n.t)("Enter duration in seconds"),onChange:l})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires."))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Table cache timeout")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"number",name:"table_cache_timeout",value:(null==e||null==(p=e.extra_json)||null==(u=p.metadata_cache_timeout)?void 0:u.table_cache_timeout)||"",placeholder:(0,n.t)("Enter duration in seconds"),onChange:l})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. "))),(0,L.tZ)(se,{css:(0,L.iv)({no_margin_bottom:K},"","")},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_run_async",indeterminate:!1,checked:!(null==e||!e.allow_run_async),onChange:t,labelText:(0,n.t)("Asynchronous query execution")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}))),(0,L.tZ)(se,{css:(0,L.iv)({no_margin_bottom:K},"","")},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==e||null==(h=e.extra_json)||!h.cancel_query_on_windows_unload),onChange:l,labelText:(0,n.t)("Cancel query on window unload event")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})))),(0,L.tZ)(Q.Z.Panel,{header:(0,L.tZ)("div",null,(0,L.tZ)("h4",null,"Security"),(0,L.tZ)("p",{className:"helper"},"Add extra connection information.")),key:"3"},(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Secure extra")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(de,{name:"encrypted_extra",value:(null==e?void 0:e.encrypted_extra)||"",placeholder:(0,n.t)("Secure extra"),onChange:e=>o({json:e,name:"encrypted_extra"}),width:"100%",height:"160px"})),(0,L.tZ)("div",{className:"helper"},(0,L.tZ)("div",null,(0,n.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Root certificate")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,n.t)("Enter CA_BUNDLE"),onChange:a})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines."))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Schemas allowed for CSV upload")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==e||null==(m=e.extra_json)?void 0:m.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("A comma-separated list of schemas that CSVs are allowed to upload to."))),(0,L.tZ)(se,{css:(0,L.iv)({no_margin_bottom:K},"","")},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:t,labelText:(0,n.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")}))),(0,L.tZ)(se,{css:(0,L.iv)({...K},"","")},(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(B.Z,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:t,labelText:(0,n.t)("Allow data upload")}),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("If selected, please set the schemas allowed for data upload in Extra.")})))),(0,L.tZ)(Q.Z.Panel,{header:(0,L.tZ)("div",null,(0,L.tZ)("h4",null,"Other"),(0,L.tZ)("p",{className:"helper"},"Additional settings.")),key:"4"},(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Metadata Parameters")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(de,{name:"metadata_params",value:(null==e||null==(g=e.extra_json)?void 0:g.metadata_params)||"",placeholder:(0,n.t)("Metadata Parameters"),onChange:e=>i({json:e,name:"metadata_params"}),width:"100%",height:"160px"})),(0,L.tZ)("div",{className:"helper"},(0,L.tZ)("div",null,(0,n.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Engine Parameters")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(de,{name:"engine_params",value:(null==e||null==(b=e.extra_json)?void 0:b.engine_params)||"",placeholder:(0,n.t)("Engine Parameters"),onChange:e=>i({json:e,name:"engine_params"}),width:"100%",height:"160px"})),(0,L.tZ)("div",{className:"helper"},(0,L.tZ)("div",null,(0,n.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Version")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"number",name:"version",value:(null==e||null==(v=e.extra_json)?void 0:v.version)||"",placeholder:(0,n.t)("Version number"),onChange:l})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Specify the database version. This should be used with Presto in order to enable query cost estimation.")))))};var _e=a(8911);const Ce=({db:e,onInputChange:t,testConnection:a,conf:o,isEditMode:l=!1,testInProgress:r=!1})=>{let s,d;var c,p;return _e.Z&&(s=null==(c=_e.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:c.SQLALCHEMY_DOCS_URL,d=null==(p=_e.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:p.SQLALCHEMY_DOCS_URL),(0,L.tZ)(i.Fragment,null,(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Display Name"),(0,L.tZ)("span",{className:"required"},"*")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:(0,n.t)("Name your database"),onChange:t})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Pick a name to help you identify this database."))),(0,L.tZ)(se,null,(0,L.tZ)("div",{className:"control-label"},(0,n.t)("SQLAlchemy URI"),(0,L.tZ)("span",{className:"required"},"*")),(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(0,n.t)("dialect+driver://username:password@host:port/database"),onChange:t})),(0,L.tZ)("div",{className:"helper"},(0,n.t)("Refer to the")," ",(0,L.tZ)("a",{href:s||(null==o?void 0:o.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer"},d||(null==o?void 0:o.SQLALCHEMY_DISPLAY_TEXT)||"")," ",(0,n.t)("for more information on how to structure your URI."))),(0,L.tZ)(N.Z,{onClick:a,disabled:r,cta:!0,buttonStyle:"link",css:e=>(e=>L.iv`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e)},(0,n.t)("Test connection")))};var we=a(87858);const Ne={account:{helpText:(0,n.t)("Copy the account name of that database you are trying to connect to."),placeholder:"e.g. world_population"},warehouse:{placeholder:"e.g. compute_wh",className:"form-group-w-50"},role:{placeholder:"e.g. AccountAdmin",className:"form-group-w-50"}},$e=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:o,field:l})=>{var i;return(0,L.tZ)(we.Z,{id:l,name:l,required:e,value:null==o||null==(i=o.parameters)?void 0:i[l],validationMethods:{onBlur:a},errorMessage:null==n?void 0:n[l],placeholder:Ne[l].placeholder,helpText:Ne[l].helpText,label:l,onChange:t.onParametersChange,className:Ne[l].className||l})};var Se=a(2857);const Ee={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M864 256H736v-80c0-35.3-28.7-64-64-64H352c-35.3 0-64 28.7-64 64v80H160c-17.7 0-32 14.3-32 32v32c0 4.4 3.6 8 8 8h60.4l24.7 523c1.6 34.1 29.8 61 63.9 61h454c34.2 0 62.3-26.8 63.9-61l24.7-523H888c4.4 0 8-3.6 8-8v-32c0-17.7-14.3-32-32-32zm-200 0H360v-72h304v72z"}}]},name:"delete",theme:"filled"};var ke=a(27029),Te=function(e,t){return i.createElement(ke.Z,Object.assign({},e,{ref:t,icon:Ee}))};Te.displayName="DeleteFilled";const Ae=i.forwardRef(Te);var Ue;!function(e){e[e.jsonUpload=0]="jsonUpload",e[e.copyPaste=1]="copyPaste"}(Ue||(Ue={}));const Oe={gsheets:"service_account_info",bigquery:"credentials_info"};var Le={name:"s5xdrg",styles:"display:flex;align-items:center"};const Me=({changeMethods:e,isEditMode:t,db:a,editNewDb:o})=>{var l,r,s;const[d,c]=(0,i.useState)(Ue.jsonUpload.valueOf()),[p,u]=(0,i.useState)(null),[h,m]=(0,i.useState)(!0),g="gsheets"===(null==a?void 0:a.engine)?!t&&!h:!t,b=t&&"{}"!==(null==a?void 0:a.encrypted_extra),v=(null==a?void 0:a.engine)&&Oe[a.engine],y="object"==typeof(null==a||null==(l=a.parameters)?void 0:l[v])?JSON.stringify(null==a||null==(r=a.parameters)?void 0:r[v]):null==a||null==(s=a.parameters)?void 0:s[v];return(0,L.tZ)(be,null,"gsheets"===(null==a?void 0:a.engine)&&(0,L.tZ)("div",{className:"catalog-type-select"},(0,L.tZ)(Se.Z,{css:e=>(e=>L.iv`
  margin-bottom: ${2*e.gridUnit}px;
`)(e),required:!0},(0,n.t)("Type of Google Sheets allowed")),(0,L.tZ)(_.Ph,{style:{width:"100%"},defaultValue:b?"false":"true",onChange:e=>m("true"===e)},(0,L.tZ)(_.Ph.Option,{value:"true",key:1},(0,n.t)("Publicly shared sheets only")),(0,L.tZ)(_.Ph.Option,{value:"false",key:2},(0,n.t)("Public and privately shared sheets")))),g&&(0,L.tZ)(i.Fragment,null,(0,L.tZ)(Se.Z,{required:!0},(0,n.t)("How do you want to enter service account credentials?")),(0,L.tZ)(_.Ph,{defaultValue:d,style:{width:"100%"},onChange:e=>c(e)},(0,L.tZ)(_.Ph.Option,{value:Ue.jsonUpload},(0,n.t)("Upload JSON file")),(0,L.tZ)(_.Ph.Option,{value:Ue.copyPaste},(0,n.t)("Copy and Paste JSON credentials")))),d===Ue.copyPaste||t||o?(0,L.tZ)("div",{className:"input-container"},(0,L.tZ)(Se.Z,{required:!0},(0,n.t)("Service Account")),(0,L.tZ)("textarea",{className:"input-form",name:v,value:y,onChange:e.onParametersChange,placeholder:"Paste content of service credentials JSON file here"}),(0,L.tZ)("span",{className:"label-paste"},(0,n.t)("Copy and paste the entire service account .json file here"))):g&&(0,L.tZ)("div",{className:"input-container",css:e=>G(e)},(0,L.tZ)("div",{css:Le},(0,L.tZ)(Se.Z,{required:!0},(0,n.t)("Upload Credentials")),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Use the JSON file you automatically downloaded when creating your service account."),viewBox:"0 0 24 24"})),!p&&(0,L.tZ)(_.zx,{className:"input-upload-btn",onClick:()=>{var e,t;return null==(e=document)||null==(t=e.getElementById("selectedFile"))?void 0:t.click()}},(0,n.t)("Choose File")),p&&(0,L.tZ)("div",{className:"input-upload-current"},p,(0,L.tZ)(Ae,{onClick:()=>{u(null),e.onParametersChange({target:{name:v,value:""}})}})),(0,L.tZ)("input",{id:"selectedFile",className:"input-upload",type:"file",onChange:async t=>{var a,n;let o;t.target.files&&(o=t.target.files[0]),u(null==(a=o)?void 0:a.name),e.onParametersChange({target:{type:null,name:v,value:await(null==(n=o)?void 0:n.text()),checked:!1}}),document.getElementById("selectedFile").value=null}})))},qe={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M563.8 512l262.5-312.9c4.4-5.2.7-13.1-6.1-13.1h-79.8c-4.7 0-9.2 2.1-12.3 5.7L511.6 449.8 295.1 191.7c-3-3.6-7.5-5.7-12.3-5.7H203c-6.8 0-10.5 7.9-6.1 13.1L459.4 512 196.9 824.9A7.95 7.95 0 00203 838h79.8c4.7 0 9.2-2.1 12.3-5.7l216.5-258.1 216.5 258.1c3 3.6 7.5 5.7 12.3 5.7h79.8c6.8 0 10.5-7.9 6.1-13.1L563.8 512z"}}]},name:"close",theme:"outlined"};var Pe=function(e,t){return i.createElement(ke.Z,Object.assign({},e,{ref:t,icon:qe}))};Pe.displayName="CloseOutlined";const De=i.forwardRef(Pe),Re=["host","port","database","username","password","database_name","credentials_info","service_account_info","catalog","query","encryption","account","warehouse","role"],Ie={host:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>{var i;return(0,L.tZ)(we.Z,{id:"host",name:"host",value:null==l||null==(i=l.parameters)?void 0:i.host,required:e,hasTooltip:!0,tooltipText:(0,n.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.host,placeholder:(0,n.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,n.t)("Host"),onChange:t.onParametersChange})},port:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>{var r;return(0,L.tZ)(i.Fragment,null,(0,L.tZ)(we.Z,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(r=l.parameters)?void 0:r.port,validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.port,placeholder:(0,n.t)("e.g. 5432"),className:"form-group-w-50",label:"Port",onChange:t.onParametersChange}))},database:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>{var i;return(0,L.tZ)(we.Z,{id:"database",name:"database",required:e,value:null==l||null==(i=l.parameters)?void 0:i.database,validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.database,placeholder:(0,n.t)("e.g. world_population"),label:(0,n.t)("Database name"),onChange:t.onParametersChange,helpText:(0,n.t)("Copy the name of the  database you are trying to connect to.")})},username:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>{var i;return(0,L.tZ)(we.Z,{id:"username",name:"username",required:e,value:null==l||null==(i=l.parameters)?void 0:i.username,validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.username,placeholder:(0,n.t)("e.g. Analytics"),label:(0,n.t)("Username"),onChange:t.onParametersChange})},password:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l,isEditMode:i})=>{var r;return(0,L.tZ)(we.Z,{id:"password",name:"password",required:e,type:i&&"password",value:null==l||null==(r=l.parameters)?void 0:r.password,validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.password,placeholder:(0,n.t)("e.g. ********"),label:(0,n.t)("Password"),onChange:t.onParametersChange})},database_name:({changeMethods:e,getValidation:t,validationErrors:a,db:o})=>(0,L.tZ)(i.Fragment,null,(0,L.tZ)(we.Z,{id:"database_name",name:"database_name",required:!0,value:null==o?void 0:o.database_name,validationMethods:{onBlur:t},errorMessage:null==a?void 0:a.database_name,placeholder:"",label:(0,n.t)("Display Name"),onChange:e.onChange,helpText:(0,n.t)("Pick a nickname for this database to display as in Superset.")})),query:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>(0,L.tZ)(we.Z,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:a},errorMessage:null==o?void 0:o.query,placeholder:(0,n.t)("e.g. param1=value1&param2=value2"),label:(0,n.t)("Additional Parameters"),onChange:t.onQueryChange,helpText:(0,n.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:t,db:a,sslForced:o})=>{var l;return(0,L.tZ)("div",{css:e=>G(e)},(0,L.tZ)(_.rs,{disabled:o&&!e,checked:(null==a||null==(l=a.parameters)?void 0:l.encryption)||o,onChange:e=>{t.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,L.tZ)("span",{css:X},"SSL"),(0,L.tZ)(z.Z,{tooltip:(0,n.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"}))},credentials_info:Me,service_account_info:Me,catalog:({required:e,changeMethods:t,getValidation:a,validationErrors:o,db:l})=>{const r=(null==l?void 0:l.catalog)||[],s=o||{};return(0,L.tZ)(Ze,null,(0,L.tZ)("h4",{className:"gsheet-title"},(0,n.t)("Connect Google Sheets as tables to this database")),(0,L.tZ)("div",null,null==r?void 0:r.map(((o,l)=>{var d,c;return(0,L.tZ)(i.Fragment,null,(0,L.tZ)(Se.Z,{className:"catalog-label",required:!0},(0,n.t)("Google Sheet Name and URL")),(0,L.tZ)("div",{className:"catalog-name"},(0,L.tZ)(we.Z,{className:"catalog-name-input",required:e,validationMethods:{onBlur:a},errorMessage:null==(d=s[l])?void 0:d.name,placeholder:(0,n.t)("Enter a name for this sheet"),onChange:e=>{t.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:o.name}),(null==r?void 0:r.length)>1&&(0,L.tZ)(De,{className:"catalog-delete",onClick:()=>t.onRemoveTableCatalog(l)})),(0,L.tZ)(we.Z,{className:"catalog-name-url",required:e,validationMethods:{onBlur:a},errorMessage:null==(c=s[l])?void 0:c.url,placeholder:(0,n.t)("Paste the shareable Google Sheet URL here"),onChange:e=>t.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:o.value}))})),(0,L.tZ)(ye,{className:"catalog-add-btn",onClick:()=>{t.onAddTableCatalog()}},"+ ",(0,n.t)("Add sheet"))))},warehouse:$e,role:$e,account:$e},ze=({dbModel:{parameters:e},onParametersChange:t,onChange:a,onQueryChange:n,onParametersUploadFileChange:o,onAddTableCatalog:l,onRemoveTableCatalog:r,validationErrors:s,getValidation:d,db:c,isEditMode:p=!1,sslForced:u,editNewDb:h})=>(0,L.tZ)(i.Fragment,null,(0,L.tZ)("div",{css:e=>[ee,re(e)]},e&&Re.filter((t=>Object.keys(e.properties).includes(t)||"database_name"===t)).map((i=>{var m;return Ie[i]({required:null==(m=e.required)?void 0:m.includes(i),changeMethods:{onParametersChange:t,onChange:a,onQueryChange:n,onParametersUploadFileChange:o,onAddTableCatalog:l,onRemoveTableCatalog:r},validationErrors:s,getValidation:d,db:c,key:i,field:i,isEditMode:p,sslForced:u,editNewDb:h})})))),Fe=(0,c.z)(),je=Fe?Fe.support:"https://superset.apache.org/docs/databases/installing-database-drivers",He={postgresql:"https://superset.apache.org/docs/databases/postgres",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},Be=e=>e?Fe?Fe[e]||Fe.default:He[e]?He[e]:`https://superset.apache.org/docs/databases/${e}`:null,Qe=({isLoading:e,isEditMode:t,useSqlAlchemyForm:a,hasConnectedDb:n,db:o,dbName:l,dbModel:r,editNewDb:s})=>{const d=(0,L.tZ)(Y,null,(0,L.tZ)(me,null,null==o?void 0:o.backend),(0,L.tZ)(ge,null,l)),c=(0,L.tZ)(Y,null,(0,L.tZ)("p",{className:"helper-top"}," STEP 2 OF 2 "),(0,L.tZ)("h4",null,"Enter Primary Credentials"),(0,L.tZ)("p",{className:"helper-bottom"},"Need help? Learn how to connect your database"," ",(0,L.tZ)("a",{href:(null==Fe?void 0:Fe.default)||je,target:"_blank",rel:"noopener noreferrer"},"here"),".")),p=(0,L.tZ)(fe,null,(0,L.tZ)(Y,null,(0,L.tZ)("p",{className:"helper-top"}," STEP 3 OF 3 "),(0,L.tZ)("h4",{className:"step-3-text"},"Your database was successfully connected! Here are some optional settings for your database"),(0,L.tZ)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",(0,L.tZ)("a",{href:Be(null==o?void 0:o.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",r.name,".")))),u=(0,L.tZ)(fe,null,(0,L.tZ)(Y,null,(0,L.tZ)("p",{className:"helper-top"}," STEP 2 OF 3 "),(0,L.tZ)("h4",null,"Enter the required ",r.name," credentials"),(0,L.tZ)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",(0,L.tZ)("a",{href:Be(null==o?void 0:o.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",r.name,".")))),h=(0,L.tZ)(Y,null,(0,L.tZ)("div",{className:"select-db"},(0,L.tZ)("p",{className:"helper-top"}," STEP 1 OF 3 "),(0,L.tZ)("h4",null,"Select a database to connect")));return e?(0,L.tZ)(i.Fragment,null):t?d:a?c:n&&!s?p:o||s?u:h},Ve={gsheets:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},Ke={CONNECTION_MISSING_PARAMETERS_ERROR:{message:(0,n.t)("Missing Required Fields"),description:(0,n.t)("Please complete all required fields.")},CONNECTION_INVALID_HOSTNAME_ERROR:{message:(0,n.t)("Could not verify the host"),description:(0,n.t)("The host is invalid. Please verify that this field is entered correctly.")},CONNECTION_PORT_CLOSED_ERROR:{message:(0,n.t)("Port is closed"),description:(0,n.t)("Please verify that port is open to connect.")},CONNECTION_INVALID_PORT_ERROR:{message:(0,n.t)("Invalid Port Number"),description:(0,n.t)("The port must be a whole number less than or equal to 65535.")},CONNECTION_ACCESS_DENIED_ERROR:{message:(0,n.t)("Invalid account information"),description:(0,n.t)("Either the username or password is incorrect.")},CONNECTION_INVALID_PASSWORD_ERROR:{message:(0,n.t)("Invalid account information"),description:(0,n.t)("Either the username or password is incorrect.")},INVALID_PAYLOAD_SCHEMA_ERROR:{message:(0,n.t)("Incorrect Fields"),description:(0,n.t)("Please make sure all fields are filled out correctly")},TABLE_DOES_NOT_EXIST_ERROR:{message:(0,n.t)("URL could not be identified"),description:(0,n.t)('The URL could not be identified. Please check for typos and make sure that "Type of google sheet allowed" selection matches the input')}};var Ye;function Je(e,t){var a,n,o,l;const i={...e||{}};let r,s={},d="",c={};switch(t.type){case Ye.extraEditorChange:return{...i,extra_json:{...i.extra_json,[t.payload.name]:t.payload.json}};case Ye.extraInputChange:var p;return"schema_cache_timeout"===t.payload.name||"table_cache_timeout"===t.payload.name?{...i,extra_json:{...i.extra_json,metadata_cache_timeout:{...null==(p=i.extra_json)?void 0:p.metadata_cache_timeout,[t.payload.name]:t.payload.value}}}:"schemas_allowed_for_file_upload"===t.payload.name?{...i,extra_json:{...i.extra_json,schemas_allowed_for_file_upload:(t.payload.value||"").split(",")}}:{...i,extra_json:{...i.extra_json,[t.payload.name]:"checkbox"===t.payload.type?t.payload.checked:t.payload.value}};case Ye.inputChange:return"checkbox"===t.payload.type?{...i,[t.payload.name]:t.payload.checked}:{...i,[t.payload.name]:t.payload.value};case Ye.parametersChange:if(void 0!==i.catalog&&null!=(a=t.payload.type)&&a.startsWith("catalog")){var u,h;const e=null==(u=t.payload.type)?void 0:u.split("-")[1];((null==i?void 0:i.catalog[e])||{})[t.payload.name]=t.payload.value;const a={};return null==(h=i.catalog)||h.map((e=>{a[e.name]=e.value})),{...i,parameters:{...i.parameters,catalog:a}}}return{...i,parameters:{...i.parameters,[t.payload.name]:t.payload.value}};case Ye.addTableCatalogSheet:return void 0!==i.catalog?{...i,catalog:[...i.catalog,{name:"",value:""}]}:{...i,catalog:[{name:"",value:""}]};case Ye.removeTableCatalogSheet:return null==(n=i.catalog)||n.splice(t.payload.indexToDelete,1),{...i};case Ye.editorChange:return{...i,[t.payload.name]:t.payload.json};case Ye.queryChange:return{...i,parameters:{...i.parameters,query:Object.fromEntries(new URLSearchParams(t.payload.value))},query_input:t.payload.value};case Ye.textChange:return{...i,[t.payload.name]:t.payload.value};case Ye.fetched:var m,g,b;if(t.payload.extra&&(r={...JSON.parse(t.payload.extra||"")},c={...JSON.parse(t.payload.extra||""),metadata_params:JSON.stringify(null==(m=r)?void 0:m.metadata_params),engine_params:JSON.stringify(null==(g=r)?void 0:g.engine_params),schemas_allowed_for_file_upload:null==(b=r)?void 0:b.schemas_allowed_for_file_upload}),s=(null==(o=t.payload)||null==(l=o.parameters)?void 0:l.query)||{},d=Object.entries(s).map((([e,t])=>`${e}=${t}`)).join("&"),t.payload.encrypted_extra&&t.payload.configuration_method===I.DYNAMIC_FORM){var v,y;const e=Object.keys((null==(v=r)||null==(y=v.engine_params)?void 0:y.catalog)||{}).map((e=>{var t,a;return{name:e,value:null==(t=r)||null==(a=t.engine_params)?void 0:a.catalog[e]}}));return{...t.payload,engine:t.payload.backend||i.engine,configuration_method:t.payload.configuration_method,extra_json:c,catalog:e,parameters:t.payload.parameters,query_input:d}}return{...t.payload,encrypted_extra:t.payload.encrypted_extra||"",engine:t.payload.backend||i.engine,configuration_method:t.payload.configuration_method,extra_json:c,parameters:t.payload.parameters,query_input:d};case Ye.dbSelected:case Ye.configMethodChange:return{...t.payload};case Ye.reset:default:return null}}!function(e){e[e.configMethodChange=0]="configMethodChange",e[e.dbSelected=1]="dbSelected",e[e.editorChange=2]="editorChange",e[e.fetched=3]="fetched",e[e.inputChange=4]="inputChange",e[e.parametersChange=5]="parametersChange",e[e.reset=6]="reset",e[e.textChange=7]="textChange",e[e.extraInputChange=8]="extraInputChange",e[e.extraEditorChange=9]="extraEditorChange",e[e.addTableCatalogSheet=10]="addTableCatalogSheet",e[e.removeTableCatalogSheet=11]="removeTableCatalogSheet",e[e.queryChange=12]="queryChange"}(Ye||(Ye={}));const We=e=>JSON.stringify({...e,metadata_params:JSON.parse((null==e?void 0:e.metadata_params)||"{}"),engine_params:JSON.parse((null==e?void 0:e.engine_params)||"{}"),schemas_allowed_for_file_upload:((null==e?void 0:e.schemas_allowed_for_file_upload)||[]).filter((e=>""!==e))}),Ge=(0,u.Z)((({addDangerToast:e,addSuccessToast:t,onDatabaseAdd:a,onHide:o,show:l,databaseId:s,dbEngine:p})=>{var u;const[h,m]=(0,i.useReducer)(Je,null),[g,b]=(0,i.useState)("1"),[v,y]=(0,c.cb)(),[f,Z,$]=(0,c.h1)(),[S,E]=(0,i.useState)(!1),[k,T]=(0,i.useState)(""),[A,U]=(0,i.useState)(!1),[O,M]=(0,i.useState)(!1),[q,P]=(0,i.useState)(!1),D=(0,F.c)(),j=(0,c.rM)(),H=(0,c.jb)(),B=!!s,Q=(0,d.c)(d.T.FORCE_DATABASE_CONNECTIONS_SSL),V=H||!(null==h||!h.engine||!Ve[h.engine]),K=(null==h?void 0:h.configuration_method)===I.SQLALCHEMY_URI,Y=B||K,{state:{loading:X,resource:ee,error:re},fetchResource:se,createResource:de,updateResource:ce,clearError:me}=(0,c.LE)("database",(0,n.t)("database"),e),ge=f||re,be=e=>e&&0===Object.keys(e).length,Ze=(null==v||null==(u=v.databases)?void 0:u.find((e=>e.engine===(B?null==h?void 0:h.backend:null==h?void 0:h.engine))))||{},_e=()=>{m({type:Ye.reset}),E(!1),$(null),me(),U(!1),o()},we=async()=>{var e;const{id:o,...l}=h||{},i=JSON.parse(JSON.stringify(l));if(i.configuration_method===I.DYNAMIC_FORM){if(await Z(i,!0),f&&!be(f))return;const e=B?i.parameters_schema.properties:null==Ze?void 0:Ze.parameters.properties,t=JSON.parse(i.encrypted_extra||"{}");Object.keys(e||{}).forEach((a=>{var n,o,l,r;e[a]["x-encrypted-extra"]&&null!=(n=i.parameters)&&n[a]&&("object"==typeof(null==(o=i.parameters)?void 0:o[a])?(t[a]=null==(l=i.parameters)?void 0:l[a],i.parameters[a]=JSON.stringify(i.parameters[a])):t[a]=JSON.parse((null==(r=i.parameters)?void 0:r[a])||"{}"))})),i.encrypted_extra=JSON.stringify(t),"gsheets"===i.engine&&(i.impersonate_user=!0)}null!=i&&null!=(e=i.parameters)&&e.catalog&&(i.extra_json={engine_params:JSON.stringify({catalog:i.parameters.catalog})}),null!=i&&i.extra_json&&(i.extra=We(null==i?void 0:i.extra_json)),null!=h&&h.id?(M(!0),await ce(h.id,i,i.configuration_method===I.DYNAMIC_FORM)&&(a&&a(),A||(_e(),t((0,n.t)("Database settings updated"))))):h&&(M(!0),await de(i,i.configuration_method===I.DYNAMIC_FORM)&&(E(!0),a&&a(),Y&&(_e(),t((0,n.t)("Database connected"))))),U(!1),M(!1)},Ne=(e,t)=>{m({type:e,payload:t})},$e=e=>{if("Other"===e)m({type:Ye.dbSelected,payload:{database_name:e,configuration_method:I.SQLALCHEMY_URI,engine:void 0}});else{const t=null==v?void 0:v.databases.filter((t=>t.name===e))[0],{engine:a,parameters:n}=t,o=void 0!==n;m({type:Ye.dbSelected,payload:{database_name:e,engine:a,configuration_method:o?I.DYNAMIC_FORM:I.SQLALCHEMY_URI}})}m({type:Ye.addTableCatalogSheet})},Se=()=>{ee&&se(ee.id),U(!0)},Ee=()=>{A&&E(!1),m({type:Ye.reset})},ke=()=>h?!S||A?(0,L.tZ)(i.Fragment,null,(0,L.tZ)(ye,{key:"back",onClick:Ee},(0,n.t)("Back")),(0,L.tZ)(ye,{key:"submit",buttonStyle:"primary",onClick:we},(0,n.t)("Connect"))):(0,L.tZ)(i.Fragment,null,(0,L.tZ)(ye,{key:"back",onClick:Se},(0,n.t)("Back")),(0,L.tZ)(ye,{key:"submit",buttonStyle:"primary",onClick:we},(0,n.t)("Finish"))):[];(0,i.useEffect)((()=>{l&&(b("1"),y(),M(!0)),s&&l&&B&&s&&(X||se(s).catch((t=>e((0,n.t)("Sorry there was an error fetching database information: %s",t.message)))))}),[l,s]),(0,i.useEffect)((()=>{ee&&(m({type:Ye.fetched,payload:ee}),T(ee.database_name))}),[ee]),(0,i.useEffect)((()=>{O&&M(!1),v&&p&&$e(p)}),[v]);const Te=()=>{if(be(re)||be(f)&&!((null==f?void 0:f.error_type)in Ke))return(0,L.tZ)(i.Fragment,null);var e,t;if(f)return(0,L.tZ)(C.Z,{type:"error",css:e=>oe(e),message:(null==(e=Ke[null==f?void 0:f.error_type])?void 0:e.message)||(null==f?void 0:f.error_type),description:(null==(t=Ke[null==f?void 0:f.error_type])?void 0:t.description)||JSON.stringify(f),showIcon:!0,closable:!1});const a="object"==typeof re?Object.values(re):[];return(0,L.tZ)(C.Z,{type:"error",css:e=>oe(e),message:(0,n.t)("Database Creation Error"),description:(null==a?void 0:a[0])||re})};return Y?(0,L.tZ)(w.Z,{css:e=>[J,W,te(e),le(e),ie(e)],name:"database",onHandledPrimaryAction:we,onHide:_e,primaryButtonName:B?(0,n.t)("Save"):(0,n.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,L.tZ)("h4",null,B?(0,n.t)("Edit database"):(0,n.t)("Connect a database")),footer:B?(0,L.tZ)(i.Fragment,null,(0,L.tZ)(ye,{key:"close",onClick:_e},(0,n.t)("Close")),(0,L.tZ)(ye,{key:"submit",buttonStyle:"primary",onClick:we},(0,n.t)("Finish"))):ke()},(0,L.tZ)(fe,null,(0,L.tZ)(he,null,(0,L.tZ)(Qe,{isLoading:O,isEditMode:B,useSqlAlchemyForm:K,hasConnectedDb:S,db:h,dbName:k,dbModel:Ze}))),(0,L.tZ)(x.ZP,{defaultActiveKey:"1",activeKey:g,onTabClick:e=>{b(e)},animated:{inkBar:!0,tabPane:!0}},(0,L.tZ)(x.ZP.TabPane,{tab:(0,L.tZ)("span",null,(0,n.t)("Basic")),key:"1"},K?(0,L.tZ)(pe,null,(0,L.tZ)(Ce,{db:h,onInputChange:({target:e})=>Ne(Ye.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:D,testConnection:()=>{var a;if(null==h||!h.sqlalchemy_uri)return void e((0,n.t)("Please enter a SQLAlchemy URI to test"));const o={sqlalchemy_uri:(null==h?void 0:h.sqlalchemy_uri)||"",database_name:(null==h||null==(a=h.database_name)?void 0:a.trim())||void 0,impersonate_user:(null==h?void 0:h.impersonate_user)||void 0,extra:We(null==h?void 0:h.extra_json)||void 0,encrypted_extra:(null==h?void 0:h.encrypted_extra)||"",server_cert:(null==h?void 0:h.server_cert)||void 0};P(!0),(0,c.xx)(o,(t=>{P(!1),e(t)}),(e=>{P(!1),t(e)}))},isEditMode:B,testInProgress:q}),(Ue=(null==h?void 0:h.backend)||(null==h?void 0:h.engine),void 0!==(null==v||null==(Oe=v.databases)||null==(Le=Oe.find((e=>e.backend===Ue||e.engine===Ue)))?void 0:Le.parameters)&&!B&&(0,L.tZ)("div",{css:e=>G(e)},(0,L.tZ)(N.Z,{buttonStyle:"link",onClick:()=>m({type:Ye.configMethodChange,payload:{database_name:null==h?void 0:h.database_name,configuration_method:I.DYNAMIC_FORM,engine:null==h?void 0:h.engine}}),css:e=>(e=>L.iv`
  font-weight: 400;
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e)},(0,n.t)("Connect this database using the dynamic form instead")),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})))):(0,L.tZ)(ze,{isEditMode:!0,sslForced:Q,dbModel:Ze,db:h,onParametersChange:({target:e})=>Ne(Ye.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>Ne(Ye.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>Ne(Ye.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>m({type:Ye.addTableCatalogSheet}),onRemoveTableCatalog:e=>m({type:Ye.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>Z(h),validationErrors:f}),!B&&(0,L.tZ)(ne,null,(0,L.tZ)(C.Z,{closable:!1,css:e=>ae(e),message:"Additional fields may be required",showIcon:!0,description:(0,L.tZ)(i.Fragment,null,(0,n.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,L.tZ)("a",{href:je,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},(0,n.t)("here")),"."),type:"info"}))),(0,L.tZ)(x.ZP.TabPane,{tab:(0,L.tZ)("span",null,(0,n.t)("Advanced")),key:"2"},(0,L.tZ)(xe,{db:h,onInputChange:({target:e})=>Ne(Ye.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Ne(Ye.textChange,{name:e.name,value:e.value}),onEditorChange:e=>Ne(Ye.editorChange,e),onExtraInputChange:({target:e})=>{Ne(Ye.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{Ne(Ye.extraEditorChange,e)}}),ge&&Te()))):(0,L.tZ)(w.Z,{css:e=>[W,te(e),le(e),ie(e)],name:"database",onHandledPrimaryAction:we,onHide:_e,primaryButtonName:S?(0,n.t)("Finish"):(0,n.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,L.tZ)("h4",null,(0,n.t)("Connect a database")),footer:ke()},S?(0,L.tZ)(i.Fragment,null,(0,L.tZ)(Qe,{isLoading:O,isEditMode:B,useSqlAlchemyForm:K,hasConnectedDb:S,db:h,dbName:k,dbModel:Ze,editNewDb:A}),A?(0,L.tZ)(ze,{isEditMode:!0,sslForced:Q,dbModel:Ze,db:h,onParametersChange:({target:e})=>Ne(Ye.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>Ne(Ye.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>Ne(Ye.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>m({type:Ye.addTableCatalogSheet}),onRemoveTableCatalog:e=>m({type:Ye.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>Z(h),validationErrors:f}):(0,L.tZ)(xe,{db:h,onInputChange:({target:e})=>Ne(Ye.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Ne(Ye.textChange,{name:e.name,value:e.value}),onEditorChange:e=>Ne(Ye.editorChange,e),onExtraInputChange:({target:e})=>{Ne(Ye.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>Ne(Ye.extraEditorChange,e)})):(0,L.tZ)(i.Fragment,null,!O&&(h?(0,L.tZ)(i.Fragment,null,(0,L.tZ)(Qe,{isLoading:O,isEditMode:B,useSqlAlchemyForm:K,hasConnectedDb:S,db:h,dbName:k,dbModel:Ze}),V&&(()=>{var e,t,a,n,o;const{hostname:l}=window.location;let i=(null==H||null==(e=H.REGIONAL_IPS)?void 0:e.default)||"";const r=(null==H?void 0:H.REGIONAL_IPS)||{};return Object.entries(r).forEach((([e,t])=>{const a=new RegExp(e);l.match(a)&&(i=t)})),(null==h?void 0:h.engine)&&(0,L.tZ)(ne,null,(0,L.tZ)(C.Z,{closable:!1,css:e=>ae(e),type:"info",showIcon:!0,message:(null==(t=Ve[h.engine])?void 0:t.message)||(null==H||null==(a=H.DEFAULT)?void 0:a.message),description:(null==(n=Ve[h.engine])?void 0:n.description)||(null==H||null==(o=H.DEFAULT)?void 0:o.description)+i}))})(),(0,L.tZ)(ze,{db:h,sslForced:Q,dbModel:Ze,onAddTableCatalog:()=>{m({type:Ye.addTableCatalogSheet})},onQueryChange:({target:e})=>Ne(Ye.queryChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{m({type:Ye.removeTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:({target:e})=>Ne(Ye.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>Ne(Ye.textChange,{name:e.name,value:e.value}),getValidation:()=>Z(h),validationErrors:f}),(0,L.tZ)("div",{css:e=>G(e)},(0,L.tZ)(N.Z,{buttonStyle:"link",onClick:()=>m({type:Ye.configMethodChange,payload:{engine:h.engine,configuration_method:I.SQLALCHEMY_URI,database_name:h.database_name}}),css:ue},(0,n.t)("Connect this database with a SQLAlchemy URI string instead")),(0,L.tZ)(z.Z,{tooltip:(0,n.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})),ge&&Te()):(0,L.tZ)(ve,null,(0,L.tZ)(Qe,{isLoading:O,isEditMode:B,useSqlAlchemyForm:K,hasConnectedDb:S,db:h,dbName:k,dbModel:Ze}),(0,L.tZ)("div",{className:"preferred"},null==v||null==(Ae=v.databases)?void 0:Ae.filter((e=>e.preferred)).map((e=>(0,L.tZ)(R,{className:"preferred-item",onClick:()=>$e(e.name),buttonText:e.name,icon:null==j?void 0:j[e.engine]})))),(()=>{var e,t;return(0,L.tZ)("div",{className:"available"},(0,L.tZ)("h4",{className:"available-label"},(0,n.t)("Or choose from a list of other databases we support:")),(0,L.tZ)("div",{className:"control-label"},(0,n.t)("Supported databases")),(0,L.tZ)(_.Ph,{className:"available-select",onChange:$e,placeholder:(0,n.t)("Choose a database...")},null==(e=[...(null==v?void 0:v.databases)||[]])?void 0:e.sort(((e,t)=>e.name.localeCompare(t.name))).map((e=>(0,L.tZ)(_.Ph.Option,{value:e.name,key:e.name},e.name))),(0,L.tZ)(_.Ph.Option,{value:"Other",key:"Other"},(0,n.t)("Other"))),(0,L.tZ)(C.Z,{showIcon:!0,closable:!1,css:e=>ae(e),type:"info",message:(null==H||null==(t=H.ADD_DATABASE)?void 0:t.message)||(0,n.t)("Want to add a new database?"),description:null!=H&&H.ADD_DATABASE?(0,L.tZ)(i.Fragment,null,(0,n.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,L.tZ)("a",{href:null==H?void 0:H.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer"},null==H?void 0:H.ADD_DATABASE.contact_description_link)," ",null==H?void 0:H.ADD_DATABASE.description):(0,L.tZ)(i.Fragment,null,(0,n.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,L.tZ)("a",{href:je,target:"_blank",rel:"noopener noreferrer"},(0,n.t)("here")),".")}))})()))),O&&(0,L.tZ)(r.Z,null));var Ae,Ue,Oe,Le})),Xe=(0,n.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),et=(0,n.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),tt=(0,o.iK)(b.Z.Check)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,at=(0,o.iK)(b.Z.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,nt=o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.base};

  .action-button {
    display: inline-block;
    height: 100%;
  }
`;function ot({value:e}){return e?(0,L.tZ)(tt,null):(0,L.tZ)(at,null)}const lt=(0,u.Z)((function({addDangerToast:e,addSuccessToast:t}){const{state:{loading:a,resourceCount:o,resourceCollection:u},hasPerm:x,fetchData:_,refreshData:C}=(0,c.Yi)("database",(0,n.t)("database"),e),[w,N]=(0,i.useState)(!1),[$,S]=(0,i.useState)(null),[E,k]=(0,i.useState)(null),[T,A]=(0,i.useState)(!1),[U,O]=(0,i.useState)([]),[M,q]=(0,i.useState)(!1);function P({database:e=null,modalOpen:t=!1}={}){k(e),N(t)}const D=x("can_write"),R=x("can_write"),I=x("can_write"),z=x("can_export")&&(0,s.cr)(d.T.VERSIONED_EXPORT),F={activeChild:"Databases",...y.Y};D&&(F.buttons=[{"data-test":"btn-create-database",name:(0,L.tZ)(i.Fragment,null,(0,L.tZ)("i",{className:"fa fa-plus"})," ",(0,n.t)("Database")," "),buttonStyle:"primary",onClick:()=>{P({modalOpen:!0})}}],(0,s.cr)(d.T.VERSIONED_EXPORT)&&F.buttons.push({name:(0,L.tZ)(g.u,{id:"import-tooltip",title:(0,n.t)("Import databases"),placement:"bottomRight"},(0,L.tZ)(b.Z.Import,null)),buttonStyle:"link",onClick:()=>{A(!0)}}));const j=(0,i.useMemo)((()=>[{accessor:"database_name",Header:(0,n.t)("Database")},{accessor:"backend",Header:(0,n.t)("Backend"),size:"lg",disableSortBy:!0},{accessor:"allow_run_async",Header:(0,L.tZ)(g.u,{id:"allow-run-async-header-tooltip",title:(0,n.t)("Asynchronous query execution"),placement:"top"},(0,L.tZ)("span",null,(0,n.t)("AQE"))),Cell:({row:{original:{allow_run_async:e}}})=>(0,L.tZ)(ot,{value:e}),size:"sm"},{accessor:"allow_dml",Header:(0,L.tZ)(g.u,{id:"allow-dml-header-tooltip",title:(0,n.t)("Allow data manipulation language"),placement:"top"},(0,L.tZ)("span",null,(0,n.t)("DML"))),Cell:({row:{original:{allow_dml:e}}})=>(0,L.tZ)(ot,{value:e}),size:"sm"},{accessor:"allow_file_upload",Header:(0,n.t)("CSV upload"),Cell:({row:{original:{allow_file_upload:e}}})=>(0,L.tZ)(ot,{value:e}),size:"md"},{accessor:"expose_in_sqllab",Header:(0,n.t)("Expose in SQL Lab"),Cell:({row:{original:{expose_in_sqllab:e}}})=>(0,L.tZ)(ot,{value:e}),size:"md"},{accessor:"created_by",disableSortBy:!0,Header:(0,n.t)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:(0,n.t)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>R||I||z?(0,L.tZ)(nt,{className:"actions"},I&&(0,L.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return t=e,l.Z.get({endpoint:`/api/v1/database/${t.id}/related_objects/`}).then((({json:e={}})=>{S({...t,chart_count:e.charts.count,dashboard_count:e.dashboards.count,sqllab_tab_count:e.sqllab_tab_states.count})})).catch((0,p.v$)((e=>(0,n.t)("An error occurred while fetching database related data: %s",e))));var t}},(0,L.tZ)(g.u,{id:"delete-action-tooltip",title:(0,n.t)("Delete database"),placement:"bottom"},(0,L.tZ)(b.Z.Trash,null))),z&&(0,L.tZ)(g.u,{id:"export-action-tooltip",title:(0,n.t)("Export"),placement:"bottom"},(0,L.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{var t;void 0!==(t=e).id&&((0,Z.Z)("database",[t.id],(()=>{q(!1)})),q(!0))}},(0,L.tZ)(b.Z.Share,null))),R&&(0,L.tZ)(g.u,{id:"edit-action-tooltip",title:(0,n.t)("Edit"),placement:"bottom"},(0,L.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>P({database:e,modalOpen:!0})},(0,L.tZ)(b.Z.EditAlt,null)))):null,Header:(0,n.t)("Actions"),id:"actions",hidden:!R&&!I,disableSortBy:!0}]),[I,R,z]),H=(0,i.useMemo)((()=>[{Header:(0,n.t)("Expose in SQL Lab"),id:"expose_in_sqllab",input:"select",operator:v.p.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:(0,L.tZ)(g.u,{id:"allow-run-async-filter-header-tooltip",title:(0,n.t)("Asynchronous query execution"),placement:"top"},(0,L.tZ)("span",null,(0,n.t)("AQE"))),id:"allow_run_async",input:"select",operator:v.p.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:(0,n.t)("Search"),id:"database_name",input:"search",operator:v.p.contains}]),[]);return(0,L.tZ)(i.Fragment,null,(0,L.tZ)(h.Z,F),(0,L.tZ)(Ge,{databaseId:null==E?void 0:E.id,show:w,onHide:P,onDatabaseAdd:()=>{C()}}),$&&(0,L.tZ)(m.Z,{description:(0,n.t)("The database %s is linked to %s charts that appear on %s dashboards and users have %s SQL Lab tabs using this database open. Are you sure you want to continue? Deleting the database will break those objects.",$.database_name,$.chart_count,$.dashboard_count,$.sqllab_tab_count),onConfirm:()=>{$&&function({id:a,database_name:o}){l.Z.delete({endpoint:`/api/v1/database/${a}`}).then((()=>{C(),t((0,n.t)("Deleted: %s",o)),S(null)}),(0,p.v$)((t=>e((0,n.t)("There was an issue deleting %s: %s",o,t)))))}($)},onHide:()=>S(null),open:!0,title:(0,n.t)("Delete Database?")}),(0,L.tZ)(v.Z,{className:"database-list-view",columns:j,count:o,data:u,fetchData:_,filters:H,initialSort:[{id:"changed_on_delta_humanized",desc:!0}],loading:a,pageSize:25}),(0,L.tZ)(f.Z,{resourceName:"database",resourceLabel:(0,n.t)("database"),passwordsNeededMessage:Xe,confirmOverwriteMessage:et,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{A(!1),C(),t((0,n.t)("Database imported"))},show:T,onHide:()=>{A(!1)},passwordFields:U,setPasswordFields:O}),M&&(0,L.tZ)(r.Z,null))}))},1483:(e,t,a)=>{a.d(t,{c:()=>o});var n=a(37703);function o(){return(0,n.v9)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.conf}))}}}]);