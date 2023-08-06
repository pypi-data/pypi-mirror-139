(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9083],{13433:(e,t,r)=>{"use strict";r.d(t,{Z:()=>m});var o=r(67294),n=r(45697),s=r.n(n),a=r(61988),i=r(58593),l=r(14114),d=r(10222),c=r(11965);const g={copyNode:s().node,getText:s().func,onCopyEnd:s().func,shouldShowText:s().bool,text:s().string,wrapped:s().bool,tooltipText:s().string,addDangerToast:s().func.isRequired,addSuccessToast:s().func.isRequired,hideTooltip:s().bool},p={copyNode:(0,c.tZ)("span",null,"Copy"),onCopyEnd:()=>{},shouldShowText:!0,wrapped:!0,tooltipText:(0,a.t)("Copy to clipboard"),hideTooltip:!1};var u={name:"8irbms",styles:"display:inline-flex;align-items:center"};class _ extends o.Component{constructor(e){super(e),this.copyToClipboard=this.copyToClipboard.bind(this),this.onClick=this.onClick.bind(this)}onClick(){this.props.getText?this.props.getText((e=>{this.copyToClipboard(e)})):this.copyToClipboard(this.props.text)}getDecoratedCopyNode(){return o.cloneElement(this.props.copyNode,{style:{cursor:"pointer"},onClick:this.onClick})}copyToClipboard(e){(0,d.Z)(e).then((()=>{this.props.addSuccessToast((0,a.t)("Copied to clipboard!"))})).catch((()=>{this.props.addDangerToast((0,a.t)("Sorry, your browser does not support copying. Use Ctrl / Cmd + C!"))})).finally((()=>{this.props.onCopyEnd()}))}renderTooltip(e){return(0,c.tZ)(o.Fragment,null,this.props.hideTooltip?this.getDecoratedCopyNode():(0,c.tZ)(i.u,{id:"copy-to-clipboard-tooltip",placement:"top",style:{cursor:e},title:this.props.tooltipText,trigger:["hover"]},this.getDecoratedCopyNode()))}renderNotWrapped(){return this.renderTooltip("pointer")}renderLink(){return(0,c.tZ)("span",{css:u},this.props.shouldShowText&&this.props.text&&(0,c.tZ)("span",{className:"m-r-5"},this.props.text),this.renderTooltip())}render(){const{wrapped:e}=this.props;return e?this.renderLink():this.renderNotWrapped()}}const m=(0,l.Z)(_);_.propTypes=g,_.defaultProps=p},54076:(e,t,r)=>{"use strict";r.d(t,{li:()=>i,Tb:()=>l,jy:()=>d,G9:()=>g,lo:()=>p,Mv:()=>u,cD:()=>_,EI:()=>m,fV:()=>R,Rw:()=>h});var o=r(51115),n=r(42846),s=r(31069),a=r(55786);const i="<NULL>",l="TRUE",d="FALSE",c=(0,o.bt)(n.Z.DATABASE_DATETIME);function g(e){return s.Z.post({endpoint:"/kv/store/",postPayload:{data:e}}).then((e=>`${window.location.origin+window.location.pathname}?id=${e.json.id}`))}function p(e){return null===e?i:""===e?"<empty string>":!0===e?"<true>":!1===e?"<false>":"string"!=typeof e&&e.toString?e.toString():e}function u(e,t){let r="";for(let o=0;o<e.length;o+=1){const n={};for(let r=0;r<t.length;r+=1){const s=t[r].name||t[r];e[o][s]?n[r]=e[o][s]:n[r]=e[o][parseFloat(s)]}r+=`${Object.values(n).join("\t")}\n`}return r}function _(e,t){return e&&0!==e.length&&0!==(0,a.Z)(t).length?e.map((e=>({...e,...t.reduce(((t,r)=>(null!==e[r]&&void 0!==e[r]&&(t[r]=c(e[r])),t)),{})}))):e}const m=()=>{},R=()=>{const{appVersion:e}=navigator;return e.includes("Win")?"Windows":e.includes("Mac")?"MacOS":e.includes("X11")?"UNIX":e.includes("Linux")?"Linux":"Unknown OS"},h=e=>null==e},55786:(e,t,r)=>{"use strict";function o(e){return null==e?[]:Array.isArray(e)?e:[e]}r.d(t,{Z:()=>o})},82191:(e,t,r)=>{"use strict";r.d(t,{Qc:()=>p.Z,qE:()=>u.C,zx:()=>_.Z,XZ:()=>m.Z,JX:()=>R.Z,iz:()=>h.Z,Lt:()=>d.Z,l0:()=>v.Z,rj:()=>E.ZP,HY:()=>b.Z,ZT:()=>O.Z,mp:()=>N.Z,iR:()=>T.Z,X2:()=>C.Z,T:()=>S.Z,Od:()=>c.Z,Rg:()=>f.Z,rs:()=>y.Z,Vp:()=>x.Z,mQ:()=>A.Z,u:()=>I.Z,gq:()=>Z.Z,oc:()=>i.Z,Ak:()=>k.Z,u_:()=>D.Z,bZ:()=>w.default,Ph:()=>$.default,aV:()=>U.default,UO:()=>L.Z,v2:()=>W,$t:()=>z,II:()=>B,Rn:()=>K,Kx:()=>G,$i:()=>V,yX:()=>Y});var o=r(5872),n=r.n(o),s=(r(67294),r(51995)),a=r(43865),i=r(4107),l=r(21888),d=r(16114),c=r(33860),g=r(11965),p=r(49288),u=r(51890),_=r(60404),m=r(9676),R=r(15746),h=r(27049),v=r(7646),E=r(75302),b=r(14277),O=r(59118),N=r(31183),T=r(31955),C=r(71230),S=r(19650),f=r(27220),y=r(59314),x=r(60331),A=r(88108),I=r(31097),Z=r(76310),k=r(39144),D=r(56697),w=r(4863),$=r(64749),U=r(56590),L=r(43700);r(82607),r(57011),r(67135);const M=(0,s.iK)(a.Z.Item)`
  > a {
    text-decoration: none;
  }

  &.ant-menu-item {
    height: ${({theme:e})=>7*e.gridUnit}px;
    line-height: ${({theme:e})=>7*e.gridUnit}px;
    a {
      border-bottom: none;
      transition: background-color ${({theme:e})=>e.transitionTiming}s;
      &:after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        width: 0;
        height: 3px;
        opacity: 0;
        transform: translateX(-50%);
        transition: all ${({theme:e})=>e.transitionTiming}s;
        background-color: ${({theme:e})=>e.colors.primary.base};
      }
      &:focus {
        border-bottom: none;
        background-color: transparent;
        @media (max-width: 767px) {
          background-color: ${({theme:e})=>e.colors.primary.light5};
        }
      }
    }
  }

  &.ant-menu-item,
  &.ant-dropdown-menu-item {
    span[role='button'] {
      display: inline-block;
      width: 100%;
    }
    transition-duration: 0s;
  }
`,F=(0,s.iK)(a.Z)`
  line-height: 51px;
  border: none;

  & > .ant-menu-item,
  & > .ant-menu-submenu {
    vertical-align: inherit;
    &:hover {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    &:hover {
      border-bottom: none;
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    margin: 0px;
  }

  & > .ant-menu-item > a {
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }
`,P=(0,s.iK)(a.Z.SubMenu)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  border-bottom: none;
  .ant-menu-submenu-open,
  .ant-menu-submenu-active {
    background-color: ${({theme:e})=>e.colors.primary.light5};
    .ant-menu-submenu-title {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: calc(100% - 1);
      }
    }
  }
  .ant-menu-submenu-title {
    position: relative;
    top: ${({theme:e})=>-e.gridUnit-3}px;
    &:after {
      content: '';
      position: absolute;
      bottom: -3px;
      left: 50%;
      width: 0;
      height: 3px;
      opacity: 0;
      transform: translateX(-50%);
      transition: all ${({theme:e})=>e.transitionTiming}s;
      background-color: ${({theme:e})=>e.colors.primary.base};
    }
  }
  .ant-menu-submenu-arrow {
    top: 67%;
  }
  & > .ant-menu-submenu-title {
    padding: 0 ${({theme:e})=>6*e.gridUnit}px 0
      ${({theme:e})=>3*e.gridUnit}px !important;
    span[role='img'] {
      position: absolute;
      right: ${({theme:e})=>-e.gridUnit-2}px;
      top: ${({theme:e})=>5.25*e.gridUnit}px;
      svg {
        font-size: ${({theme:e})=>6*e.gridUnit}px;
        color: ${({theme:e})=>e.colors.grayscale.base};
      }
    }
    & > span {
      position: relative;
      top: 7px;
    }
    &:hover {
      color: ${({theme:e})=>e.colors.primary.base};
    }
  }
`,W=Object.assign(a.Z,{Item:M}),z=Object.assign(F,{Item:M,SubMenu:P,Divider:a.Z.Divider,ItemGroup:a.Z.ItemGroup}),B=(0,s.iK)(i.Z)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,K=(0,s.iK)(l.Z)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,G=(0,s.iK)(i.Z.TextArea)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,V=e=>(0,g.tZ)(d.Z,n()({overlayStyle:{zIndex:99,animationDuration:"0s"}},e)),Y=(0,s.iK)(c.Z)`
  h3 {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  ul {
    margin-bottom: 0;
  }
`},82607:(e,t,r)=>{"use strict";r.d(t,{Z:()=>a}),r(67294);var o=r(51995),n=r(62529),s=r(11965);const a=(0,o.iK)((({textColor:e,...t})=>(0,s.tZ)(n.Z,t)))`
  & > sup {
    padding: 0 ${({theme:e})=>2*e.gridUnit}px;
    background: ${({theme:e,color:t})=>t||e.colors.primary.base};
    color: ${({theme:e,textColor:t})=>t||e.colors.grayscale.light5};
  }
`},35932:(e,t,r)=>{"use strict";r.d(t,{Z:()=>m});var o=r(5872),n=r.n(o),s=r(11965),a=r(21804),i=r.n(a),l=r(67294),d=r(84967),c=r(94184),g=r.n(c),p=r(60404),u=r(51995),_=r(58593);function m(e){const{tooltip:t,placement:r,disabled:o=!1,buttonSize:a,buttonStyle:c,className:m,cta:R,children:h,href:v,showMarginRight:E=!0,...b}=e,O=(0,u.Fg)(),{colors:N,transitionTiming:T,borderRadius:C,typography:S}=O,{primary:f,grayscale:y,success:x,warning:A,error:I}=N;let Z=32,k=18;"xsmall"===a?(Z=22,k=5):"small"===a&&(Z=30,k=10);let D=f.light4,w=(0,d.CD)(.1,f.base,f.light4),$=(0,d.CD)(.25,f.base,f.light4),U=y.light2,L=f.dark1,M=L,F=0,P="none",W="transparent",z="transparent",B="transparent";"primary"===c?(D=f.dark1,w=(0,d.CD)(.1,y.light5,f.dark1),$=(0,d.CD)(.2,y.dark2,f.dark1),L=y.light5,M=L):"tertiary"===c||"dashed"===c?(D=y.light5,w=y.light5,$=y.light5,U=y.light5,F=1,P="dashed"===c?"dashed":"solid",W=f.dark1,z=f.light1,B=y.light2):"danger"===c?(D=I.base,w=(0,d.CD)(.1,y.light5,I.base),$=(0,d.CD)(.2,y.dark2,I.base),L=y.light5,M=L):"warning"===c?(D=A.base,w=(0,d.CD)(.1,y.dark2,A.base),$=(0,d.CD)(.2,y.dark2,A.base),L=y.light5,M=L):"success"===c?(D=x.base,w=(0,d.CD)(.1,y.light5,x.base),$=(0,d.CD)(.2,y.dark2,x.base),L=y.light5,M=L):"link"===c&&(D="transparent",w="transparent",$="transparent",M=f.base);const K=h;let G=[];G=K&&K.type===l.Fragment?l.Children.toArray(K.props.children):l.Children.toArray(h);const V=E&&G.length>1?2*O.gridUnit:0,Y=(0,s.tZ)(p.Z,n()({href:o?void 0:v,disabled:o,className:g()(m,"superset-button",{cta:!!R}),css:(0,s.iv)({display:"inline-flex",alignItems:"center",justifyContent:"center",lineHeight:1.5715,fontSize:S.sizes.s,fontWeight:S.weights.bold,height:Z,textTransform:"uppercase",padding:`0px ${k}px`,transition:`all ${T}s`,minWidth:R?36*O.gridUnit:void 0,minHeight:R?8*O.gridUnit:void 0,boxShadow:"none",borderWidth:F,borderStyle:P,borderColor:W,borderRadius:C,color:L,backgroundColor:D,"&:hover":{color:M,backgroundColor:w,borderColor:z},"&:active":{color:L,backgroundColor:$},"&:focus":{color:L,backgroundColor:D,borderColor:W},"&[disabled], &[disabled]:hover":{color:y.base,backgroundColor:"link"===c?"transparent":U,borderColor:"link"===c?"transparent":B},marginLeft:0,"& + .superset-button":{marginLeft:2*O.gridUnit},"& > :first-of-type":{marginRight:V}},"","")},b),h);return t?(0,s.tZ)(_.u,{placement:r,id:`${i()(t)}-tooltip`,title:t},o?(0,s.tZ)("span",null,Y):Y):Y}},57011:(e,t,r)=>{"use strict";r.d(t,{Z:()=>i});var o=r(5872),n=r.n(o),s=(r(67294),r(70302)),a=r(11965);const i=({padded:e,...t})=>(0,a.tZ)(s.Z,n()({},t,{css:t=>({backgroundColor:t.colors.grayscale.light4,borderRadius:t.borderRadius,".ant-card-body":{padding:e?4*t.gridUnit:t.gridUnit}})}))},43700:(e,t,r)=>{"use strict";r.d(t,{Z:()=>a}),r(67294);var o=r(51995),n=r(46445),s=r(11965);const a=Object.assign((0,o.iK)((({light:e,bigger:t,bold:r,animateArrows:o,...a})=>(0,s.tZ)(n.Z,a)))`
    .ant-collapse-item {
      .ant-collapse-header {
        font-weight: ${({bold:e,theme:t})=>e?t.typography.weights.bold:t.typography.weights.normal};
        font-size: ${({bigger:e,theme:t})=>e?4*t.gridUnit+"px":"inherit"};

        .ant-collapse-arrow svg {
          transition: ${({animateArrows:e})=>e?"transform 0.24s":"none"};
        }

        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(90deg) !important;\n            }\n          "}

        ${({light:e,theme:t})=>e&&`\n            color: ${t.colors.grayscale.light4};\n            .ant-collapse-arrow svg {\n              color: ${t.colors.grayscale.light4};\n            }\n          `}

        ${({ghost:e,bordered:t,theme:r})=>e&&t&&`\n            border-bottom: 1px solid ${r.colors.grayscale.light3};\n          `}
      }
      .ant-collapse-content {
        .ant-collapse-content-box {
          .loading.inline {
            margin: ${({theme:e})=>12*e.gridUnit}px auto;
            display: block;
          }
        }
      }
    }
    .ant-collapse-item-active {
      .ant-collapse-header {
        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(-90deg) !important;\n            }\n          "}
      }
    }
  `,{Panel:n.Z.Panel})},91178:(e,t,r)=>{"use strict";r.d(t,{Z:()=>m});var o=r(67294),n=r(51995),s=r(61988),a=r(54076),i=r(74069),l=r(35932),d=r(70163),c=r(13433),g=r(11965);const p=n.iK.div`
  align-items: center;
  background-color: ${({level:e,theme:t})=>t.colors[e].light2};
  border-radius: ${({theme:e})=>e.borderRadius}px;
  border: 1px solid ${({level:e,theme:t})=>t.colors[e].base};
  color: ${({level:e,theme:t})=>t.colors[e].dark2};
  padding: ${({theme:e})=>2*e.gridUnit}px;
  width: 100%;

  .top-row {
    display: flex;
    justify-content: space-between;
  }

  .error-body {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-left: ${({theme:e})=>8*e.gridUnit}px;
  }

  .icon {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  .link {
    color: ${({level:e,theme:t})=>t.colors[e].dark2};
    text-decoration: underline;
  }
`,u=(0,n.iK)(i.Z)`
  color: ${({level:e,theme:t})=>t.colors[e].dark2};
  overflow-wrap: break-word;

  .ant-modal-header {
    background-color: ${({level:e,theme:t})=>t.colors[e].light2};
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }

  .icon {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  .header {
    display: flex;
    align-items: center;
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
  }
`,_=n.iK.div`
  align-items: center;
  display: flex;
`;function m({body:e,copyText:t,level:r="error",source:i="dashboard",subtitle:m,title:R}){const h=(0,n.Fg)(),[v,E]=(0,o.useState)(!1),[b,O]=(0,o.useState)(!1),N=["explore","sqllab"].includes(i),T=h.colors[r].base;return(0,g.tZ)(p,{level:r,role:"alert"},(0,g.tZ)("div",{className:"top-row"},(0,g.tZ)(_,null,"error"===r?(0,g.tZ)(d.Z.ErrorSolid,{className:"icon",iconColor:T}):(0,g.tZ)(d.Z.WarningSolid,{className:"icon",iconColor:T}),(0,g.tZ)("strong",null,R)),!N&&(0,g.tZ)("span",{role:"button",tabIndex:0,className:"link",onClick:()=>E(!0)},(0,s.t)("See more"))),N?(0,g.tZ)("div",{className:"error-body"},(0,g.tZ)("p",null,m),e&&(0,g.tZ)(o.Fragment,null,!b&&(0,g.tZ)("span",{role:"button",tabIndex:0,className:"link",onClick:()=>O(!0)},(0,s.t)("See more")),b&&(0,g.tZ)(o.Fragment,null,(0,g.tZ)("br",null),e,(0,g.tZ)("span",{role:"button",tabIndex:0,className:"link",onClick:()=>O(!1)},(0,s.t)("See less"))))):(0,g.tZ)(u,{level:r,show:v,onHide:()=>E(!1),title:(0,g.tZ)("div",{className:"header"},"error"===r?(0,g.tZ)(d.Z.ErrorSolid,{className:"icon",iconColor:T}):(0,g.tZ)(d.Z.WarningSolid,{className:"icon",iconColor:T}),(0,g.tZ)("div",{className:"title"},R)),footer:(0,g.tZ)(o.Fragment,null,t&&(0,g.tZ)(c.Z,{text:t,shouldShowText:!1,wrapped:!1,copyNode:(0,g.tZ)(l.Z,{onClick:a.EI},(0,s.t)("Copy message"))}),(0,g.tZ)(l.Z,{cta:!0,buttonStyle:"primary",onClick:()=>E(!1)},(0,s.t)("Close")))},(0,g.tZ)(o.Fragment,null,(0,g.tZ)("p",null,m),(0,g.tZ)("br",null),e)))}},92869:(e,t,r)=>{"use strict";r.d(t,{Z:()=>a});var o=r(90537),n=r(1875);class s extends o.Z{constructor(){super({name:"ErrorMessageComponent",overwritePolicy:o.r.ALLOW})}}const a=(0,n.Z)(s)},67663:(e,t,r)=>{"use strict";r.d(t,{C:()=>o});const o={FRONTEND_CSRF_ERROR:"FRONTEND_CSRF_ERROR",FRONTEND_NETWORK_ERROR:"FRONTEND_NETWORK_ERROR",FRONTEND_TIMEOUT_ERROR:"FRONTEND_TIMEOUT_ERROR",GENERIC_DB_ENGINE_ERROR:"GENERIC_DB_ENGINE_ERROR",COLUMN_DOES_NOT_EXIST_ERROR:"COLUMN_DOES_NOT_EXIST_ERROR",TABLE_DOES_NOT_EXIST_ERROR:"TABLE_DOES_NOT_EXIST_ERROR",SCHEMA_DOES_NOT_EXIST_ERROR:"SCHEMA_DOES_NOT_EXIST_ERROR",CONNECTION_INVALID_USERNAME_ERROR:"CONNECTION_INVALID_USERNAME_ERROR",CONNECTION_INVALID_PASSWORD_ERROR:"CONNECTION_INVALID_PASSWORD_ERROR",CONNECTION_INVALID_HOSTNAME_ERROR:"CONNECTION_INVALID_HOSTNAME_ERROR",CONNECTION_PORT_CLOSED_ERROR:"CONNECTION_PORT_CLOSED_ERROR",CONNECTION_INVALID_PORT_ERROR:"CONNECTION_INVALID_PORT_ERROR",CONNECTION_HOST_DOWN_ERROR:"CONNECTION_HOST_DOWN_ERROR",CONNECTION_ACCESS_DENIED_ERROR:"CONNECTION_ACCESS_DENIED_ERROR",CONNECTION_UNKNOWN_DATABASE_ERROR:"CONNECTION_UNKNOWN_DATABASE_ERROR",CONNECTION_DATABASE_PERMISSIONS_ERROR:"CONNECTION_DATABASE_PERMISSIONS_ERROR",CONNECTION_MISSING_PARAMETERS_ERRORS:"CONNECTION_MISSING_PARAMETERS_ERRORS",OBJECT_DOES_NOT_EXIST_ERROR:"OBJECT_DOES_NOT_EXIST_ERROR",SYNTAX_ERROR:"SYNTAX_ERROR",VIZ_GET_DF_ERROR:"VIZ_GET_DF_ERROR",UNKNOWN_DATASOURCE_TYPE_ERROR:"UNKNOWN_DATASOURCE_TYPE_ERROR",FAILED_FETCHING_DATASOURCE_INFO_ERROR:"FAILED_FETCHING_DATASOURCE_INFO_ERROR",TABLE_SECURITY_ACCESS_ERROR:"TABLE_SECURITY_ACCESS_ERROR",DATASOURCE_SECURITY_ACCESS_ERROR:"DATASOURCE_SECURITY_ACCESS_ERROR",DATABASE_SECURITY_ACCESS_ERROR:"DATABASE_SECURITY_ACCESS_ERROR",QUERY_SECURITY_ACCESS_ERROR:"QUERY_SECURITY_ACCESS_ERROR",MISSING_OWNERSHIP_ERROR:"MISSING_OWNERSHIP_ERROR",BACKEND_TIMEOUT_ERROR:"BACKEND_TIMEOUT_ERROR",DATABASE_NOT_FOUND_ERROR:"DATABASE_NOT_FOUND_ERROR",MISSING_TEMPLATE_PARAMS_ERROR:"MISSING_TEMPLATE_PARAMS_ERROR",INVALID_TEMPLATE_PARAMS_ERROR:"INVALID_TEMPLATE_PARAMS_ERROR",RESULTS_BACKEND_NOT_CONFIGURED_ERROR:"RESULTS_BACKEND_NOT_CONFIGURED_ERROR",DML_NOT_ALLOWED_ERROR:"DML_NOT_ALLOWED_ERROR",INVALID_CTAS_QUERY_ERROR:"INVALID_CTAS_QUERY_ERROR",INVALID_CVAS_QUERY_ERROR:"INVALID_CVAS_QUERY_ERROR",SQLLAB_TIMEOUT_ERROR:"SQLLAB_TIMEOUT_ERROR",RESULTS_BACKEND_ERROR:"RESULTS_BACKEND_ERROR",ASYNC_WORKERS_ERROR:"ASYNC_WORKERS_ERROR",GENERIC_COMMAND_ERROR:"GENERIC_COMMAND_ERROR",GENERIC_BACKEND_ERROR:"GENERIC_BACKEND_ERROR",INVALID_PAYLOAD_FORMAT_ERROR:"INVALID_PAYLOAD_FORMAT_ERROR",INVALID_PAYLOAD_SCHEMA_ERROR:"INVALID_PAYLOAD_SCHEMA_ERROR"}},70163:(e,t,r)=>{"use strict";r.d(t,{Z:()=>v});var o=r(5872),n=r.n(o),s=r(18029),a=r.n(s),i=r(67294),l=r(62816),d=r(16165),c=r(51995);function g(){return g=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e},g.apply(this,arguments)}const p=function(e){return i.createElement("svg",g({width:24,height:24,viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e))};var u=r(11965);const _=(0,c.iK)((({iconColor:e,iconSize:t,viewBox:r,...o})=>(0,u.tZ)(d.Z,n()({viewBox:r||"0 0 24 24"},o))))`
  ${({iconColor:e})=>e&&`color: ${e};`};
  font-size: ${({iconSize:e,theme:t})=>e?`${t.typography.sizes[e]||t.typography.sizes.m}px`:"24px"};
`,m=e=>{const{fileName:t,...o}=e,[,s]=(0,i.useState)(!1),a=(0,i.useRef)(),l=t.replace("_","-");return(0,i.useEffect)((()=>{let e=!1;return async function(){a.current=(await r(35782)(`./${t}.svg`)).default,e||s(!0)}(),()=>{e=!0}}),[t,a]),(0,u.tZ)(_,n()({component:a.current||p,"aria-label":l},o))},R=Object.keys(l).map((e=>({[e]:t=>(0,u.tZ)(_,n()({component:l[e]},t))}))).reduce(((e,t)=>({...e,...t}))),h={};["alert","alert_solid","alert_solid_small","binoculars","bolt","bolt_small","bolt_small_run","calendar","cancel","cancel_solid","cancel-x","card_view","cards","cards_locked","caret_down","caret_left","caret_right","caret_up","certified","check","checkbox-half","checkbox-off","checkbox-on","circle_check","circle_check_solid","circle","clock","close","code","cog","collapse","color_palette","components","copy","cursor_target","database","dataset_physical","dataset_virtual_greyscale","dataset_virtual","download","drag","edit_alt","edit","email","error","error_solid","error_solid_small","exclamation","expand","eye","eye_slash","favorite-selected","favorite_small_selected","favorite-unselected","field_abc","field_boolean","field_date","field_derived","field_num","field_struct","file","filter","filter_small","folder","full","function_x","gear","grid","image","import","info","info-solid","info_solid_small","join","keyboard","layers","lightbulb","link","list","list_view","location","lock_locked","lock_unlocked","map","message","minus","minus_solid","more_horiz","more_vert","move","nav_charts","nav_dashboard","nav_data","nav_explore","nav_home","nav_lab","note","offline","paperclip","placeholder","plus","plus_large","plus_small","plus_solid","queued","refresh","running","save","sql","search","server","share","slack","sort_asc","sort_desc","sort","table","tag","trash","triangle_change","triangle_down","triangle_up","up-level","user","warning","warning_solid","x-large","x-small","tags","ballot","category"].forEach((e=>{const t=a()(e).replace(/ /g,"");h[t]=t=>(0,u.tZ)(m,n()({fileName:e},t))}));const v={...R,...h}},37921:(e,t,r)=>{"use strict";r.d(t,{Z:()=>l});var o=r(5872),n=r.n(o),s=r(11965),a=(r(67294),r(82191)),i=r(51995);function l(e){const t=(0,i.Fg)(),{colors:r,transitionTiming:o}=t,{type:l,onClick:d,children:c,...g}=e,{primary:p,secondary:u,grayscale:_,success:m,warning:R,error:h,info:v}=r;let E=_.light3,b=d?p.light2:_.light3,O=d?_.light2:"transparent",N=d?p.light1:"transparent",T=_.dark1;if(l&&"default"!==l){let e;T=_.light4,e="success"===l?m:"warning"===l?R:"danger"===l?h:"info"===l?v:"secondary"===l?u:p,E=e.base,b=d?e.dark1:e.base,O=d?e.dark1:"transparent",N=d?e.dark2:"transparent"}return(0,s.tZ)(a.Vp,n()({onClick:d},g,{css:(0,s.iv)({transition:`background-color ${o}s`,whiteSpace:"nowrap",cursor:d?"pointer":"default",overflow:"hidden",textOverflow:"ellipsis",backgroundColor:E,borderColor:O,borderRadius:21,padding:"0.35em 0.8em",lineHeight:1,color:T,maxWidth:"100%","&:hover":{backgroundColor:b,borderColor:N,opacity:1}},"","")}),c)}},72570:(e,t,r)=>{"use strict";r.d(t,{h:()=>a,fz:()=>i,K7:()=>l,RS:()=>d,bM:()=>c,ws:()=>g,Dz:()=>p,Gb:()=>u,s2:()=>_});var o=r(14670),n=r.n(o),s=r(8818);const a="ADD_TOAST";function i({toastType:e,text:t,duration:r=8e3,noDuplicate:o=!1}){return{type:a,payload:{id:(s=e,`${s}-${n().generate()}`),toastType:e,text:t,duration:r,noDuplicate:o}};var s}const l="REMOVE_TOAST";function d(e){return{type:l,payload:{id:e}}}function c(e,t){return i({text:e,toastType:s.p.INFO,duration:4e3,...t})}function g(e,t){return i({text:e,toastType:s.p.SUCCESS,duration:4e3,...t})}function p(e,t){return i({text:e,toastType:s.p.WARNING,duration:6e3,...t})}function u(e,t){return i({text:e,toastType:s.p.DANGER,duration:8e3,...t})}const _={addInfoToast:c,addSuccessToast:g,addWarningToast:p,addDangerToast:u}},8818:(e,t,r)=>{"use strict";var o;r.d(t,{p:()=>o}),function(e){e.INFO="INFO_TOAST",e.SUCCESS="SUCCESS_TOAST",e.WARNING="WARNING_TOAST",e.DANGER="DANGER_TOAST"}(o||(o={}))},14114:(e,t,r)=>{"use strict";r.d(t,{Z:()=>l,e:()=>d});var o=r(67294),n=r(14890),s=r(37703),a=r(72570);const i={addInfoToast:a.bM,addSuccessToast:a.ws,addWarningToast:a.Dz,addDangerToast:a.Gb};function l(e){return(0,s.$j)(null,(e=>(0,n.DE)(i,e)))(e)}function d(){const e=(0,s.I0)();return(0,o.useMemo)((()=>(0,n.DE)(i,e)),[e])}},74069:(e,t,r)=>{"use strict";r.d(t,{o:()=>R,Z:()=>v});var o=r(5872),n=r.n(o),s=r(14293),a=r.n(s),i=r(67294),l=r(51995),d=r(61988),c=r(11965),g=r(82191),p=r(35932),u=r(29119),_=r(61193),m=r.n(_);const R=(0,l.iK)((e=>(0,c.tZ)(g.u_,n()({},e,{maskTransitionName:""}))))`
  ${({theme:e,responsive:t,maxWidth:r})=>t&&(0,c.iv)("max-width:",null!=r?r:"900px",";padding-left:",3*e.gridUnit,"px;padding-right:",3*e.gridUnit,"px;","")}

  .ant-modal-header {
    background-color: ${({theme:e})=>e.colors.grayscale.light4};
    border-radius: ${({theme:e})=>e.borderRadius}px
      ${({theme:e})=>e.borderRadius}px 0 0;
    padding-left: ${({theme:e})=>4*e.gridUnit}px;
    padding-right: ${({theme:e})=>4*e.gridUnit}px;

    .ant-modal-title h4 {
      display: flex;
      margin: 0;
      align-items: center;
    }
  }

  .ant-modal-close-x {
    display: flex;
    align-items: center;

    .close {
      flex: 1 1 auto;
      margin-bottom: ${({theme:e})=>e.gridUnit}px;
      color: ${({theme:e})=>e.colors.secondary.dark1};
      font-size: 32px;
      font-weight: ${({theme:e})=>e.typography.weights.light};
    }
  }

  .ant-modal-body {
    padding: ${({theme:e})=>4*e.gridUnit}px;
    overflow: auto;
    ${({resizable:e,height:t})=>!e&&t&&`height: ${t};`}
  }
  .ant-modal-footer {
    border-top: ${({theme:e})=>e.gridUnit/4}px solid
      ${({theme:e})=>e.colors.grayscale.light2};
    padding: ${({theme:e})=>4*e.gridUnit}px;

    .btn {
      font-size: 12px;
      text-transform: uppercase;
    }

    .btn + .btn {
      margin-left: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  // styling for Tabs component
  // Aaron note 20-11-19: this seems to be exclusively here for the Edit Database modal.
  // TODO: remove this as it is a special case.
  .ant-tabs-top {
    margin-top: -${({theme:e})=>4*e.gridUnit}px;
  }

  &.no-content-padding .ant-modal-body {
    padding: 0;
  }

  ${({draggable:e,theme:t})=>e&&`\n    .ant-modal-header {\n      padding: 0;\n      .draggable-trigger {\n          cursor: move;\n          padding: ${4*t.gridUnit}px;\n          width: 100%;\n        }\n    }\n  `};

  ${({resizable:e,hideFooter:t})=>e&&`\n    .resizable {\n      pointer-events: all;\n\n      .resizable-wrapper {\n        height: 100%;\n      }\n\n      .ant-modal-content {\n        height: 100%;\n\n        .ant-modal-body {\n          /* 100% - header height - footer height */\n          height: ${t?"calc(100% - 55px);":"calc(100% - 55px - 65px);"}\n        }\n      }\n    }\n  `}
`,h=({children:e,disablePrimaryButton:t=!1,onHide:r,onHandledPrimaryAction:o,primaryButtonName:s=(0,d.t)("OK"),primaryButtonType:l="primary",show:g,name:_,title:h,width:v,maxWidth:E,responsive:b=!1,centered:O,footer:N,hideFooter:T,wrapProps:C,draggable:S=!1,resizable:f=!1,resizableConfig:y={maxHeight:"100vh",maxWidth:"100vw",minHeight:T?109:174,minWidth:"380px",enable:{bottom:!0,bottomLeft:!1,bottomRight:!0,left:!1,top:!1,topLeft:!1,topRight:!1,right:!0}},draggableConfig:x,destroyOnClose:A,...I})=>{const Z=(0,i.useRef)(null),[k,D]=(0,i.useState)(),[w,$]=(0,i.useState)(!0),U=a()(N)?[(0,c.tZ)(p.Z,{key:"back",onClick:r,cta:!0},(0,d.t)("Cancel")),(0,c.tZ)(p.Z,{key:"submit",buttonStyle:l,disabled:t,onClick:o,cta:!0},s)]:N,L=v||(b?"100vw":"600px"),M=!(f||S);return(0,c.tZ)(R,n()({centered:!!O,onOk:o,onCancel:r,width:L,maxWidth:E,responsive:b,visible:g,title:(0,c.tZ)((()=>S?(0,c.tZ)("div",{className:"draggable-trigger",onMouseOver:()=>w&&$(!1),onMouseOut:()=>!w&&$(!0)},h):(0,c.tZ)(i.Fragment,null,h)),null),closeIcon:(0,c.tZ)("span",{className:"close","aria-hidden":"true"},"×"),footer:T?null:U,hideFooter:T,wrapProps:{"data-test":`${_||h}-modal`,...C},modalRender:e=>f||S?(0,c.tZ)(m(),n()({disabled:!S||w,bounds:k,onStart:(e,t)=>((e,t)=>{var r,o,n;const{clientWidth:s,clientHeight:a}=null==(r=window)||null==(o=r.document)?void 0:o.documentElement,i=null==Z||null==(n=Z.current)?void 0:n.getBoundingClientRect();i&&D({left:-(null==i?void 0:i.left)+(null==t?void 0:t.x),right:s-((null==i?void 0:i.right)-(null==t?void 0:t.x)),top:-(null==i?void 0:i.top)+(null==t?void 0:t.y),bottom:a-((null==i?void 0:i.bottom)-(null==t?void 0:t.y))})})(0,t)},x),f?(0,c.tZ)(u.e,n()({className:"resizable"},y),(0,c.tZ)("div",{className:"resizable-wrapper",ref:Z},e)):(0,c.tZ)("div",{ref:Z},e)):e,mask:M,draggable:S,resizable:f,destroyOnClose:A||f||S},I),e)};h.displayName="Modal";const v=Object.assign(h,{error:g.u_.error,warning:g.u_.warning,confirm:g.u_.confirm,useModal:g.u_.useModal})},67135:(e,t,r)=>{"use strict";r.d(t,{Z:()=>a}),r(67294);var o=r(51995),n=r(82833),s=r(11965);const a=(0,o.iK)((({striped:e,...t})=>(0,s.tZ)(n.Z,t)))`
  line-height: 0;
  position: static;
  .ant-progress-inner {
    position: static;
  }
  .ant-progress-outer {
    ${({percent:e})=>!e&&"display: none;"}
  }
  .ant-progress-text {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-progress-bg {
    position: static;
    ${({striped:e})=>e&&"\n        background-image: linear-gradient(45deg,\n            rgba(255, 255, 255, 0.15) 25%,\n            transparent 25%, transparent 50%,\n            rgba(255, 255, 255, 0.15) 50%,\n            rgba(255, 255, 255, 0.15) 75%,\n            transparent 75%, transparent) !important;\n        background-size: 1rem 1rem !important;\n        "};
  }
`},58593:(e,t,r)=>{"use strict";r.d(t,{u:()=>d});var o=r(5872),n=r.n(o),s=r(67294),a=r(51995),i=r(11965),l=r(31097);const d=e=>{const t=(0,a.Fg)();return(0,i.tZ)(s.Fragment,null,(0,i.tZ)(i.xB,{styles:i.iv`
          .ant-tooltip-open {
            display: inline-block;
            &::after {
              content: '';
              display: block;
            }
          }
        `}),(0,i.tZ)(l.Z,n()({overlayStyle:{fontSize:t.typography.sizes.s,lineHeight:"1.6"},color:`${t.colors.grayscale.dark2}e6`},e)))}},10222:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});const o=async e=>new Promise(((t,r)=>{const o=document.getSelection();if(o){o.removeAllRanges();const t=document.createRange(),n=document.createElement("span");n.textContent=e,n.style.position="fixed",n.style.top="0",n.style.clip="rect(0, 0, 0, 0)",n.style.whiteSpace="pre",document.body.appendChild(n),t.selectNode(n),o.addRange(t);try{document.execCommand("copy")||r()}catch(e){r()}document.body.removeChild(n),o.removeRange?o.removeRange(t):o.removeAllRanges()}t()}))},66785:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});const o={SESSION_TIMED_OUT:"Your session timed out, please refresh your page and try again."}},98286:(e,t,r)=>{"use strict";r.d(t,{M:()=>a,O:()=>i});var o=r(61988),n=r(67663),s=r(66785);function a(e){let t={...e};var r,n;return t.errors&&t.errors.length>0&&(t.error=t.description=t.errors[0].message,t.link=null==(r=t.errors[0])||null==(n=r.extra)?void 0:n.link),t.stack?t={...t,error:(0,o.t)("Unexpected error: ")+(t.description||(0,o.t)("(no description, click to see stack trace)")),stacktrace:t.stack}:t.responseText&&t.responseText.indexOf("CSRF")>=0&&(t={...t,error:(0,o.t)(s.Z.SESSION_TIMED_OUT)}),{...t,error:t.error}}function i(e){return new Promise((t=>{if("string"==typeof e)t({error:e});else{const r=e instanceof Response?e:e.response;if(r&&!r.bodyUsed)r.clone().json().then((e=>{const o={...r,...e};t(a(o))})).catch((()=>{r.text().then((e=>{t({...r,error:e})}))}));else if("statusText"in e&&"timeout"===e.statusText&&"timeout"in e)t({...r,error:"Request timed out",errors:[{error_type:n.C.FRONTEND_TIMEOUT_ERROR,extra:{timeout:e.timeout/1e3,issue_codes:[{code:1e3,message:(0,o.t)("Issue 1000 - The dataset is too large to query.")},{code:1001,message:(0,o.t)("Issue 1001 - The database is under an unusual load.")}]},level:"error",message:"Request timed out"}]});else{let n=e.statusText||e.message;n||(console.error("non-standard error:",e),n=(0,o.t)("An error occurred")),t({...r,error:n})}}}))}},35782:(e,t,r)=>{var o={"./alert.svg":[57249,7249],"./alert_solid.svg":[52797,2797],"./alert_solid_small.svg":[71256,1256],"./ballot.svg":[87760,7760],"./binoculars.svg":[38970,8970],"./bolt.svg":[4794,4794],"./bolt_small.svg":[49510,9510],"./bolt_small_run.svg":[36883,6883],"./calendar.svg":[65816,5816],"./cancel-x.svg":[77654,7654],"./cancel.svg":[14757,4757],"./cancel_solid.svg":[55777,5777],"./card_view.svg":[25838,5838],"./cards.svg":[81293,1293],"./cards_locked.svg":[69052,9052],"./caret_down.svg":[48820,7832],"./caret_left.svg":[80310,310],"./caret_right.svg":[64817,4817],"./caret_up.svg":[6011,9811],"./category.svg":[24851,4851],"./certified.svg":[88695,8695],"./check.svg":[83544,3544],"./checkbox-half.svg":[57405,7405],"./checkbox-off.svg":[75281,5281],"./checkbox-on.svg":[99013,9013],"./circle.svg":[60183,183],"./circle_check.svg":[93558,3558],"./circle_check_solid.svg":[70992,992],"./clock.svg":[50597,597],"./close.svg":[50999,999],"./code.svg":[16981,6981],"./cog.svg":[45962,5962],"./collapse.svg":[24266,4266],"./color_palette.svg":[65580,5580],"./components.svg":[80312,312],"./copy.svg":[23141,3141],"./cross-filter-badge.svg":[64625,4625],"./cursor_target.svg":[96758,6758],"./database.svg":[15249,5249],"./dataset_physical.svg":[8312,8312],"./dataset_virtual.svg":[77156,5330],"./dataset_virtual_greyscale.svg":[84810,4810],"./default_db_image.svg":[51398,1398],"./download.svg":[112,112],"./drag.svg":[86507,6507],"./edit.svg":[93871,3871],"./edit_alt.svg":[86167,6167],"./email.svg":[50504,6668],"./error.svg":[67584,7584],"./error_solid.svg":[25641,5641],"./error_solid_small.svg":[92561,2983],"./error_solid_small_red.svg":[4273,4273],"./exclamation.svg":[35771,5771],"./expand.svg":[47922,7922],"./eye.svg":[11493,1493],"./eye_slash.svg":[45014,9109],"./favorite-selected.svg":[51568,1568],"./favorite-unselected.svg":[86682,6682],"./favorite_small_selected.svg":[1351,1351],"./field_abc.svg":[70215,215],"./field_boolean.svg":[87405,5507],"./field_date.svg":[65226,5226],"./field_derived.svg":[37404,4732],"./field_num.svg":[35201,5201],"./field_struct.svg":[91899,1899],"./file.svg":[20057,57],"./filter.svg":[19305,9305],"./filter_small.svg":[54474,4474],"./folder.svg":[86420,6420],"./full.svg":[23985,3985],"./function_x.svg":[44662,4662],"./gear.svg":[7610,7610],"./grid.svg":[68425,8425],"./image.svg":[92264,2264],"./import.svg":[42698,2698],"./info-solid.svg":[71605,1605],"./info.svg":[2713,2713],"./info_solid_small.svg":[33606,3606],"./join.svg":[85998,5998],"./keyboard.svg":[87850,7850],"./layers.svg":[85832,5832],"./lightbulb.svg":[54797,4797],"./link.svg":[99558,9558],"./list.svg":[45707,5707],"./list_view.svg":[38682,8682],"./location.svg":[61174,1174],"./lock_locked.svg":[55359,5359],"./lock_unlocked.svg":[6207,6207],"./map.svg":[18463,8463],"./message.svg":[64458,4458],"./minus.svg":[97183,7183],"./minus_solid.svg":[6371,6371],"./more_horiz.svg":[39325,9325],"./more_vert.svg":[91185,1185],"./move.svg":[74139,4139],"./nav_charts.svg":[75350,5350],"./nav_dashboard.svg":[66303,6303],"./nav_data.svg":[2267,2267],"./nav_explore.svg":[83749,3749],"./nav_home.svg":[44667,4667],"./nav_lab.svg":[43567,3567],"./note.svg":[46597,6126],"./offline.svg":[53265,3265],"./paperclip.svg":[22079,2079],"./placeholder.svg":[18349,8349],"./plus.svg":[17460,7460],"./plus_large.svg":[66150,6150],"./plus_small.svg":[96447,6447],"./plus_solid.svg":[70600,600],"./queued.svg":[63240,3240],"./refresh.svg":[25367,5367],"./running.svg":[5224,5224],"./save.svg":[36254,6254],"./search.svg":[30177,177],"./server.svg":[11075,1075],"./share.svg":[11263,1263],"./slack.svg":[42439,2439],"./sort.svg":[20336,336],"./sort_asc.svg":[79393,9393],"./sort_desc.svg":[32646,2646],"./sql.svg":[13325,3325],"./table.svg":[72403,2403],"./tag.svg":[30158,158],"./tags.svg":[90363,363],"./transparent.svg":[87803,7803],"./trash.svg":[62105,2105],"./triangle_change.svg":[98398,8398],"./triangle_down.svg":[40826,826],"./triangle_up.svg":[36819,6819],"./up-level.svg":[65972,5972],"./user.svg":[99767,9767],"./warning.svg":[4758,4758],"./warning_solid.svg":[75224,5592],"./x-large.svg":[63955,3955],"./x-small.svg":[7716,7716]};function n(e){if(!r.o(o,e))return Promise.resolve().then((()=>{var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=o[e],n=t[0];return r.e(t[1]).then((()=>r(n)))}n.keys=()=>Object.keys(o),n.id=35782,e.exports=n}}]);