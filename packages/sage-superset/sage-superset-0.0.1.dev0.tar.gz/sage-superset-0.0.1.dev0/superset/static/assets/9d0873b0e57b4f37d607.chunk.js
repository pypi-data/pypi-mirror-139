"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9483],{89483:(e,t,r)=>{r.r(t),r.d(t,{default:()=>f});var o,a=r(751995),s=r(667294),n=r(101090),i=r(269856),l=r(174448),d=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e);var u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const c=(0,a.iK)(l.un)`
  overflow-x: auto;
`,m=a.iK.div`
  padding: 2px;
  & > span,
  & > span:hover {
    border: 2px solid transparent;
    display: inline-block;
    border: ${({theme:e,validateStatus:t})=>{var r;return t&&`2px solid ${null==(r=e.colors[t])?void 0:r.base}`}};
  }
  &:focus {
    & > span {
      border: 2px solid
        ${({theme:e,validateStatus:t})=>{var r;return t?null==(r=e.colors[t])?void 0:r.base:e.colors.primary.base}};
      outline: 0;
      box-shadow: 0 0 0 2px
        ${({validateStatus:e})=>e?"rgba(224, 67, 85, 12%)":"rgba(32, 167, 201, 0.2)"};
    }
  }
`,p=["inclusive","exclusive"];function f(e){var t;const{setDataMask:r,setFocusedFilter:o,unsetFocusedFilter:a,width:l,height:u,filterState:f,formData:{inputRef:v}}=e,h=(0,s.useCallback)((e=>{const t=e&&e!==i.vM;r({extraFormData:t?{time_range:e}:{},filterState:{value:t?e:void 0}})}),[r]);return(0,s.useEffect)((()=>{h(f.value)}),[f.value]),null!=(t=e.formData)&&t.inView?(0,d.tZ)(c,{width:l,height:u},(0,d.tZ)(m,{tabIndex:-1,ref:v,validateStatus:f.validateStatus,onFocus:o,onBlur:a,onMouseEnter:o,onMouseLeave:a},(0,d.tZ)(n.Z,{endpoints:p,value:f.value||i.vM,name:"time_range",onChange:h,type:f.validateStatus}))):null}var v,h;u(f,"useCallback{handleTimeRangeChange}\nuseEffect{}"),(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(c,"TimeFilterStyles","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx"),v.register(m,"ControlContainer","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx"),v.register(p,"endpoints","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx"),v.register(f,"TimeFilterPlugin","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx")),(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&h(e)},174448:(e,t,r)=>{r.d(t,{un:()=>n,jp:()=>i,Am:()=>l});var o,a=r(751995),s=r(804591);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const n=a.iK.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e}px;
`,i=(0,a.iK)(s.Z)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,l=a.iK.div`
  color: ${({theme:e,status:t="error"})=>{var r;return null==(r=e.colors[t])?void 0:r.base}};
`;var d,u;(d="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(d.register(n,"FilterPluginStyle","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/common.ts"),d.register(i,"StyledFormItem","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/common.ts"),d.register(l,"StatusMessage","/Users/chenming/PycharmProjects/superset/superset-frontend/src/filters/components/common.ts")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)}}]);