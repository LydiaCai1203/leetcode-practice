(window["nojMonomainWebpackJsonpproduction"]=window["nojMonomainWebpackJsonpproduction"]||[]).push([[249],{"9OSg":function(e,t,r){"use strict";r.r(t);var o=r("ERkP");var s=r.n(o);var i=r("83rr");var n=r.n(i);var a=r("D57K");var l=r("1l9P");var u=r("RNvQ");var c=r.n(u);var p=r("fsDi");var d=r("Q0jv");var f=r("8NtH");var g=r("UqMZ");var h=r("8d7B");var m=r("zRE0");var v=r("/Oqt");var S=r("oosw");var b=r("S0yW");var y=r("DjZ7");var E=r("5ZzG");var C=r("v31z");var k=r("JFCy");var O=r("LJ7e");var A=r("SwI/");var q=r("IDXw");var x=Object(O["default"])("div",{target:"e5i1odf0"})({},"label:SolutionWrapper;");var L=Object(O["default"])("div",{target:"e5i1odf1"})({width:"100%",margin:"15px 0",display:"flex",justifyContent:"center"},"label:PaginationWrapper;");var P=Object(O["default"])("div",{target:"e5i1odf2"})({height:"36px",lineHeight:"36px",display:"flex",justifyContent:"space-between",flexWrap:"nowrap","& *":{fontSize:"12px"},borderBottom:"1px solid "+A["a"].grey2},"label:OperationsWrapper;");var w=Object(O["default"])(E["a"],{target:"e5i1odf3"})({marginLeft:"20px",alignSelf:"center",minWidth:"12px",minHeight:"12px",flex:"0 0 auto"},"label:SearchIcon;");var D=Object(O["default"])("input",{target:"e5i1odf4"})({border:"none",outline:"none !important",color:A["a"].dblue8,marginLeft:"10px","&:placeholder":{color:A["a"].grey3},flex:"1 1 auto"},"label:Search;");var j=Object(O["default"])("div",{target:"e5i1odf5"})({padding:"0 20px",maxWidth:q["a"],margin:"0 auto"},"label:ArticleListWrapper;");var R=Object(O["default"])("div",{target:"e5i1odf6"})({marginLeft:"20px",marginRight:"10px",whiteSpace:"nowrap",display:"flex",alignItems:"center","> button:not(:last-child)":{marginRight:"15px"}},"label:EditWrapper;");var T=Object(O["default"])("div",{target:"e5i1odf7"})({width:"20px",display:"flex",alignItems:"center"},"label:ItemCheckedWrapper;");var W=Object(O["default"])(function(e){return s.a.createElement(b["a"],a["__assign"]({},e))},{target:"e5i1odf8"})({".ant-dropdown-menu-item-selected":{background:A["a"].dblue7,color:A["a"].white}},"label:Menu;");var I=Object(O["default"])("ul",{target:"e5i1odf9"})({width:"110px",margin:"0",padding:"0",listStyle:"none","& li":{fontSize:"12px",lineHeight:"30px",color:A["a"].red5,background:A["a"].white,textAlign:"center",cursor:"pointer","&:hover":{background:A["a"].grey1}}},"label:AdminMenu;");var M=Object(O["default"])(C["a"],{target:"e5i1odf10"})({height:"30px",color:A["a"].red5,"&:hover:not([disabled])":{color:A["a"].red5}},"label:AdminButton;");var F=Object(O["default"])("div",{target:"e5i1odf11"})({display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"200px"},"label:EmptyWrapper;");var _=Object(O["default"])("h5",{target:"e5i1odf12"})({margin:"0 0 20px",padding:"0",fontSize:"14px",color:A["a"].dark6},"label:EmptyTitle;");var V=Object(O["default"])("div",{target:"e5i1odf13"})({display:"flex",flexDirection:"column"},"label:ExtraMenu;");var B=Object(O["default"])(C["a"],{target:"e5i1odf14"})({"&, &:hover":{color:A["a"].red5}},"label:DeleteButton;");var U=r("nnm9");var z=r.n(U);function N(e){var t=e.onClick,r=t===void 0?z.a:t,i=a["__rest"](e,["onClick"]);var n=Object(o["useCallback"])(function(e){r(e)},[r]);return s.a.createElement(C["a"],a["__assign"]({},i,{onClick:n}))}var H=b["a"].Item;var K={default:{name:"默认排序",value:"DEFAULT"},favorite:{name:"点赞最多",value:"MOST_UPVOTE"},popular:{name:"热度最高",value:"HOT"},latest:{name:"最新发布",value:"NEWEST_TO_OLDEST"},earliest:{name:"最早发布",value:"OLDEST_TO_NEWEST"}};var J=function(e){a["__extends"](t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;r.state={input:"",selectedKey:K.default.value};r.onClickWriting=function(){g["a"].ensurePhoneVerified(function(){if(r.props.draftSlug){r.props.showSolutionEditorForEditingArticle(r.props.draftSlug)}else{r.props.showSolutionEditorForCreatingArticle({questionSlug:r.props.questionSlug})}},{user:r.context})()};r.onSearch=function(){r.props.onSearch(r.state.input)};r.onInput=function(e){var t=e.currentTarget;r.setState({input:t.value},function(){return r.props.onSearch(r.state.input)})};r.renderOrderMenuCheckedIcon=function(e){return s.a.createElement(T,null,r.state.selectedKey===e&&s.a.createElement(E["a"],{type:"check"}))};r.renderOrderMenu=function(){var e=s.a.createElement(W,{onClick:r.onClick,selectedKeys:[r.state.selectedKey],multiple:false},Object.values(K).map(function(e){return s.a.createElement(H,{key:e.value},r.renderOrderMenuCheckedIcon(e.value),e.name)}));return s.a.createElement(v["a"],{overlay:e,trigger:["click"]},s.a.createElement(C["a"],{type:"transparent",icon:"rank",size:k["e"]},"排序"))};r.onClick=function(e){var t=e.key;return r.setState({selectedKey:t},function(){return r.props.onChangeOrder(t)})};return r}t.prototype.render=function(){return s.a.createElement(P,null,s.a.createElement(w,{type:"search",onClick:this.onSearch}),s.a.createElement(D,{disabled:this.props.disabled,placeholder:"搜索题解",onInput:this.onInput}),s.a.createElement(R,null,this.renderOrderMenu(),!this.props.isEditing&&s.a.createElement(N,{type:"primary",icon:"add",size:k["e"],onClick:this.onClickWriting,disabled:this.props.disabled},this.props.draftSlug?"继续写题解":"写题解")))};t.contextType=h["userContext"];return t}(s.a.PureComponent);var Q=r("zCf4");var Y=r("nPqx");var Z=r("YnYl");var G=r("u+Aj");var X=r("sYqU");var $=r("TqBM");var ee=r("pnSG");var te=r("excc");var re=r("FLAH");var ie=r("DuHN");var ne=r("IJu9");var oe=r("/usP");var ae=function(e){a["__extends"](t,e);function t(){var t=e!==null&&e.apply(this,arguments)||this;t.state={withdrawVisible:false,deleteConfirmVisible:false};t.onWithdrawOk=function(){t.props.setSolutionArticleAsWithdrawed(t.props.article.slug)};t.renderEditorsPick=function(){var e=t.props.article.isEditorsPick;return s.a.createElement("li",{onClick:t.onClickEditorPick},e?"取消精选":"设为精选")};t.onClickEditorPick=function(){return t.props.setSolutionArticleAsEditorsPick({slug:t.props.article.slug,value:!t.props.article.isEditorsPick})};t.renderOfficialPick=function(){var e=t.props.article.byLeetcode;return s.a.createElement("li",{onClick:t.onClickOfficialPick},e?"取消官方":"设为官方")};t.onClickOfficialPick=function(){return t.props.setSolutionArticleAsOfficial({slug:t.props.article.slug,value:!t.props.article.byLeetcode})};t.renderDelete=function(){var e=t.props.article.status===Z["e"].Removed;return s.a.createElement("li",{onClick:t.onClickDelete},e?"恢复删除":"删除")};t.onDelete=function(){t.props.setSolutionArticleAsRemoved({slug:t.props.article.slug,value:t.props.article.status!==Z["e"].Removed});t.onCloseDelete()};t.onClickDelete=function(){return t.setState({deleteConfirmVisible:true})};t.onCloseDelete=function(){return t.setState({deleteConfirmVisible:false})};t.renderMenu=function(){return s.a.createElement(I,null,t.renderEditorsPick(),t.renderOfficialPick(),t.renderDelete(),s.a.createElement("li",{onClick:t.onShowWithdraw},"下线"))};t.onShowWithdraw=function(){return t.setState({withdrawVisible:true})};t.onCloseWithdraw=function(){return t.setState({withdrawVisible:false})};return t}t.prototype.componentDidUpdate=function(e){if(!e.adminOperationResult.message&&!!this.props.adminOperationResult.message&&this.props.adminOperationResult.slug===this.props.article.slug){ie["a"].error(this.props.adminOperationResult.message);this.props.resetAdminOperationResult()}};t.prototype.render=function(){return s.a.createElement(s.a.Fragment,null,s.a.createElement(te["a"],{trigger:"click",content:this.renderMenu(),placement:"bottom"},s.a.createElement(M,{type:"transparent",icon:"settings"})),s.a.createElement(oe["a"],{visible:this.state.withdrawVisible,warningText:"文章下线后将退回至用户草稿",resourceType:t.resourceType,resourceId:this.props.article.identifier,onClose:this.onCloseWithdraw,flagStatus:Z["l"].EditRequested,onOk:this.onWithdrawOk}),s.a.createElement(Y["a"],{visible:this.state.deleteConfirmVisible,type:"threat",onOk:this.onDelete,onClose:this.onCloseDelete},"您确认要",this.props.article.status===Z["e"].Removed?"恢复":"删除","这篇题解吗？"))};t.resourceType=Z["r"].Article;return t}(s.a.PureComponent);var le=function(e){return{adminOperationResult:e.solution.adminOperationResult}};var se=Object(l["a"])(m["c"])(le)(ae);var ue=function(e){a["__extends"](l,e);function l(){var n=e!==null&&e.apply(this,arguments)||this;n.state={report:{visible:false,resourceId:null},deleteModalVisible:false,deleteSlug:null};n.onDelete=function(){n.state.deleteSlug&&n.props.deleteSolutionArticle({questionSlug:n.props.questionSlug,slug:n.state.deleteSlug,callback:function(){return n.props.getArticleList()}})};n.onCloseDeleteModal=function(){return n.setState({deleteModalVisible:false})};n.onClickDelete=function(e){f["a"].questionDetail.solutionListClickDelete({questionSlug:n.props.questionSlug});n.setState({deleteModalVisible:true,deleteSlug:e.currentTarget.dataset.contentId})};n.onReact=function(e){var t=e.reactedWith,r=e.contentId,i=e.prevReactedWith;g["a"].ensureVerified(function(){if(i&&t===i){f["a"].questionDetail.solutionListRemoveReaction({questionSlug:n.props.questionSlug});n.props.removeReaction(r)}else{f["a"].questionDetail.solutionListAddReaction({questionSlug:n.props.questionSlug,reactionType:t});n.props.addReaction({articleSlug:r,reactionType:t})}},{user:n.props.userStatus})()};n.onClickFavor=function(e,t){g["a"].ensureVerified(function(){if(e){f["a"].questionDetail.solutionListAddFavoriteArticle({questionSlug:n.props.questionSlug});n.props.addFavoriteArticle(t)}else{f["a"].questionDetail.solutionListRemoveFavoriteArticle({questionSlug:n.props.questionSlug});n.props.removeFavoriteArticle(t)}},{user:n.props.userStatus})()};n.onUpvote=function(e,t){g["a"].ensureVerified(function(){if(e){f["a"].questionDetail.solutionListUpvoteArticle({questionSlug:n.props.questionSlug});n.props.upvoteArticle(t)}else{f["a"].questionDetail.solutionListCancelUpvoteArticle({questionSlug:n.props.questionSlug});n.props.cancelUpvoteArticle(t)}},{user:n.props.userStatus})()};n.onClickComment=function(e,t){f["a"].questionDetail.solutionListClickComment({questionSlug:n.props.questionSlug});n.props.history.push(X["a"].questionSolution(t,e,"#comment"))};n.onClickEdit=function(e){var t=e.currentTarget;f["a"].questionDetail.solutionListClickEdit({questionSlug:n.props.questionSlug});t.dataset.contentId&&n.props.showSolutionEditorForEditingArticle(t.dataset.contentId)};n.onClickReport=function(e){var t=e.currentTarget;f["a"].questionDetail.solutionListClickReport({questionSlug:n.props.questionSlug});n.setState({report:{visible:true,resourceId:t.dataset.identifier||null}})};n.onClose=function(){n.setState({report:{visible:false,resourceId:null}})};return n}l.prototype.render=function(){var e=this.state,t=e.report,r=e.deleteModalVisible;var i=this.props,n=i.userStatus,o=i.articles;var a=!!n&&n.isAdmin;return s.a.createElement(s.a.Fragment,null,s.a.createElement($["a"],{renderAdminMenu:a?this.renderAdminMenu:undefined,articles:this.getDisplayedArticles(o)}),s.a.createElement(G["a"],{visible:t.visible,resourceId:t.resourceId,resourceType:l.reportType,onClose:this.onClose}),s.a.createElement(Y["a"],{type:"threat",visible:r,onOk:this.onDelete,onClose:this.onCloseDeleteModal},"您确定删除该题解吗？"))};l.prototype.renderAdminMenu=function(e,t){return s.a.createElement(se,{resourceId:e,article:t})};l.prototype.renderReactionExtraMenu=function(e,t,r){return s.a.createElement(V,null,t&&s.a.createElement(B,{size:"xs",type:"transparent","data-content-id":e,"data-identifier":r,onClick:this.onClickDelete},"删除"),s.a.createElement(C["a"],{size:"xs",type:"transparent","data-content-id":e,"data-identifier":r,onClick:t?this.onClickEdit:this.onClickReport},t?"编辑":"举报"))};l.prototype.getDisplayedArticles=function(e){var t=this;return e.map(function(e){return{article:e,relatedQuestion:{questionSlug:t.props.questionSlug},reaction:{contentId:e.slug,upvote:{count:e.upvoteCount,upvoted:e.upvoted,onClick:t.onUpvote},emoji:a["__assign"]({onReact:t.onReact,reactedWith:e.reactedType?e.reactedType:null},function(){if(!e.reactions||!e.reactions.length)return{};var t=new Map;e.reactions.forEach(function(e){return t.set(e.reactionType,e.count)});return{countMap:t}}()),comment:{count:e.topic?e.topic.commentCount:0,extraData:t.props.questionSlug,onClick:t.onClickComment},share:{type:"copyLink",config:{shareConfig:{title:e.title+" - 我分享的「"+document.title+"」题解",link:Object(ee["a"])({articleSlug:e.slug,questionSlug:t.props.questionSlug})}}},favor:{favored:e.isMyFavorite,onClick:t.onClickFavor},extraMenu:t.renderReactionExtraMenu(e.slug,e.canEdit,e.identifier)}}})};l.reportType=Z["r"].Article;return l}(s.a.PureComponent);var ce=Object(Q["withRouter"])(ue);var pe=r("K/af");var de=r("thsd");var fe=r("aH7E");function ge(e){var t=a["__read"](Object(pe["a"])(fe["a"]),1),r=t[0].question;var i=r.translatedTitle||r.title;var n=e.articles.slice(0,3).map(function(e,t){var r=e.title,i=e.author,n=e.summary;return t+1+". 标题: "+r+" 作者:"+i.username+" 摘要:"+n}).join("; ");if(!i){return null}return s.a.createElement(de["a"],{title:"题解 - "+i,description:n})}var he=function(e){a["__extends"](r,e);function r(){var t=e!==null&&e.apply(this,arguments)||this;t.state={current:1,orderBy:K.default.value,input:"",searchedCurrent:1,searchedOrderBy:K.default.value};t.onClickWriting=g["a"].ensureVerified(function(){if(t.draftSlug){t.props.showSolutionEditorForEditingArticle(t.draftSlug)}else{t.props.showSolutionEditorForCreatingArticle({questionSlug:t.props.questionSlug})}},{user:t.context});t.onSearch=c()(function(e){t.setState({input:e},function(){return t.props.getSearchedArticleList({questionSlug:t.props.questionSlug,first:r.numPerPage,skip:(t.state.searchedCurrent-1)*r.numPerPage,orderBy:t.state.searchedOrderBy||undefined,userInput:t.state.input})})},300);t.onChange=function(e){if(t.isSearching){t.setState({searchedCurrent:e},t.getArticleList)}else{t.setState({current:e},t.getArticleList)}};t.onChangeOrder=function(e){f["a"].questionDetail.changeSolutionListOrder({orderBy:e});if(t.isSearching){t.setState({searchedOrderBy:e},t.getArticleList)}else{t.setState({orderBy:e},t.getArticleList)}};t.getArticleList=function(){if(t.isSearching){t.props.getSearchedArticleList({questionSlug:t.props.questionSlug,first:r.numPerPage,skip:(t.state.searchedCurrent-1)*r.numPerPage,orderBy:t.state.searchedOrderBy,input:t.state.input})}else{t.props.getArticleList({questionSlug:t.props.questionSlug,first:r.numPerPage,skip:(t.state.current-1)*r.numPerPage,orderBy:t.state.orderBy})}};return t}Object.defineProperty(r.prototype,"isSearching",{get:function(){return!!this.state.input.length},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"totalNum",{get:function(){return this.isSearching?this.props.solutions.searchedArticleList.totalNum:this.props.solutions.articleList.totalNum},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"articles",{get:function(){return this.isSearching?this.props.solutions.searchedArticleList.articles:this.props.solutions.articleList.articles},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"current",{get:function(){return this.isSearching?this.state.searchedCurrent:this.state.current},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"draft",{get:function(){var r=this;var e=this.props.solutions.draftList.articles;return e.filter(function(e){var t=e.question;return t.questionTitleSlug===r.props.questionSlug})},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"loading",{get:function(){return this.props.solutions.articleList.loading||this.props.solutions.draftList.loading},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"isEmptyList",{get:function(){return!this.loading&&this.props.solutions.articleList.totalNum===0},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"draftSlug",{get:function(){return this.draft.length?this.draft[0].slug:null},enumerable:true,configurable:true});Object.defineProperty(r.prototype,"isEditing",{get:function(){return this.props.solutionAreaShownPart===m["a"].EDITOR||this.props.solutionAreaShownPart===m["a"].WILL_CLOSE_EDITOR},enumerable:true,configurable:true});r.prototype.componentDidMount=function(){this.props.getDraftList(this.props.questionSlug);this.getArticleList()};r.prototype.componentWillUnmount=function(){this.props.disposeArticleList$()};r.prototype.render=function(){return s.a.createElement(s.a.Fragment,null,s.a.createElement(ge,{articles:this.props.solutions.articleList.articles}),this.isEmptyList?this.renderEmpty():s.a.createElement(x,null,s.a.createElement(J,{disabled:this.loading,questionSlug:this.props.questionSlug,onChangeOrder:this.onChangeOrder,onSearch:this.onSearch,draftSlug:this.draftSlug,showSolutionEditorForEditingArticle:this.props.showSolutionEditorForEditingArticle,showSolutionEditorForCreatingArticle:this.props.showSolutionEditorForCreatingArticle,isEditing:this.isEditing}),this.loading?s.a.createElement(p["a"],{size:"xs"}):s.a.createElement(s.a.Fragment,null,s.a.createElement(ce,{articles:this.articles,questionSlug:this.props.questionSlug,userStatus:this.context,addFavoriteArticle:this.props.addFavoriteArticle,removeFavoriteArticle:this.props.removeFavoriteArticle,upvoteArticle:this.props.upvoteArticle,cancelUpvoteArticle:this.props.cancelUpvoteArticle,addReaction:this.props.addReaction,removeReaction:this.props.removeReaction,showSolutionEditorForEditingArticle:this.props.showSolutionEditorForEditingArticle,deleteSolutionArticle:this.props.deleteSolutionArticle,getArticleList:this.getArticleList}),s.a.createElement(L,null,s.a.createElement(d["a"],{current:this.current,totalNum:this.totalNum,onChange:this.onChange,numPerPage:r.numPerPage})))))};r.prototype.renderEmpty=function(){return s.a.createElement(F,null,s.a.createElement(_,null,"当前题目暂无题解"),s.a.createElement(N,{icon:"edit",onClick:this.onClickWriting},this.draftSlug?"继续写题解":"写题解"))};r.contextType=h["userContext"];r.numPerPage=10;return r}(s.a.PureComponent);var me=function(e){var t=e.solution;return t};var ve=Object(l["a"])(m["c"])(me)(he);var Se=t["default"]=Object(o["memo"])(function(){var e=n()().match;return s.a.createElement(ve,{questionSlug:e.params.questionSlug})})}}]);