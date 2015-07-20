//Maya ASCII 2014 scene
//Name: testing.ma
//Last modified: Mon, Jul 20, 2015 03:29:17 PM
//Codeset: 1252
requires maya "2014";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2014";
fileInfo "version" "2014";
fileInfo "cutIdentifier" "201310090514-890429";
fileInfo "osv" "Microsoft Windows 7 Home Premium Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "character_grp";
	addAttr -ci true -sn "moduleMaintenanceVisibility" -ln "moduleMaintenanceVisibility" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "animationControlVisibility" -ln "animationControlVisibility" 
		-dv 1 -min 0 -max 1 -at "bool";
	setAttr ".moduleMaintenanceVisibility";
	setAttr -k on ".animationControlVisibility";
lockNode -l 1 -lu 1;
createNode transform -n "HingeJoint__instance_1:module_grp" -p "character_grp";
	addAttr -ci true -sn "hierarchicalScale" -ln "hierarchicalScale" -at "float";
lockNode -l 1 -lu 1;
createNode transform -n "HingeJoint__instance_1:HOOK_IN" -p "HingeJoint__instance_1:module_grp";
	setAttr ".s";
	setAttr ".sy";
lockNode -l 1 -lu 1;
createNode transform -n "HingeJoint__instance_1:blueprint_joints_grp" -p "HingeJoint__instance_1:HOOK_IN";
	addAttr -ci true -sn "controlModuleInstalled" -ln "controlModuleInstalled" -min 
		0 -max 1 -at "bool";
	setAttr ".ove" yes;
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:blueprint_root_joint" -p "HingeJoint__instance_1:blueprint_joints_grp";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.9999998004611 14.036423091218621 0 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 -50 0 ;
	setAttr ".bps" -type "matrix" 0.97014173978704799 0 -0.24253866644920694 0 8.4466777113566349e-010 -1 3.3786260682818239e-009 0
		 -0.24253866644920694 -3.48261076677667e-009 -0.97014173978704821 0 0 0 0 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:blueprint_hinge_joint" -p "HingeJoint__instance_1:blueprint_root_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 4.123105525970459 0 5.5511151231257827e-016 ;
	setAttr ".t";
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 28.072846182437303 0 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 50 0 ;
	setAttr ".bps" -type "matrix" 0.97014173978704776 1.6388949220632047e-009 0.24253866644920805 0
		 8.4466777113566349e-010 -1 3.3786260682818239e-009 0 0.24253866644920793 -3.0728815771689324e-009 -0.97014173978704787 0
		 3.9999967682905728 -1.9332373295414649e-024 -1.0000125158982316 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:blueprint_end_joint" -p "HingeJoint__instance_1:blueprint_hinge_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 4.123105525970459 3.4578755056242158e-025 8.8817841970012523e-016 ;
	setAttr ".t";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.97014173978704776 1.6388949220632047e-009 0.24253866644920805 0
		 8.4466777113566349e-010 -1 3.3786260682818239e-009 0 0.24253866644920793 -3.0728815771689324e-009 -0.97014173978704787 0
		 7.9999935365811448 6.7573367096437194e-009 3.1086244689504383e-015 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode transform -n "HingeJoint__instance_1:creationPose_joint_grp" -p "HingeJoint__instance_1:HOOK_IN";
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:creationPose_root_joint" -p "HingeJoint__instance_1:creationPose_joint_grp";
	setAttr ".v" no;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.9999998004611 14.036423091218621 0 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 -50 0 ;
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:creationPose_hinge_joint" -p "HingeJoint__instance_1:creationPose_root_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 4.123105525970459 0 5.5511151231257827e-016 ;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 28.072846182437303 0 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 50 0 ;
lockNode -l 1 -lu 1;
createNode joint -n "HingeJoint__instance_1:creationPose_end_joint" -p "HingeJoint__instance_1:creationPose_hinge_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 4.123105525970459 3.4578755056242158e-025 8.8817841970012523e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode transform -n "HingeJoint__instance_1:SETTINGS" -p "HingeJoint__instance_1:module_grp";
	addAttr -ci true -sn "activeModule" -ln "activeModule" -min 0 -max 0 -en "None" 
		-at "enum";
	addAttr -ci true -sn "creationPoseWeight" -ln "creationPoseWeight" -dv 1 -at "float";
	setAttr ".v" no;
lockNode -l 1 -lu 1;
createNode locator -n "HingeJoint__instance_1:SETTINGSShape" -p "HingeJoint__instance_1:SETTINGS";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode transform -n "non_blueprint_grp" -p "character_grp";
	addAttr -ci true -k true -sn "display" -ln "display" -dv 1 -min 0 -max 1 -at "bool";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".rp" -type "double3" 4.0774678903275481 -2.327689164749458e-007 -3.491533773214428e-007 ;
	setAttr ".sp" -type "double3" 4.0774678903275481 -2.327689164749458e-007 -3.491533773214428e-007 ;
	setAttr -k on ".display";
lockNode -l 1 -lu 1;
createNode transform -n "pCylinder1" -p "non_blueprint_grp";
	setAttr ".t" -type "double3" 4.0774678903275481 1.8107594936045626e-015 0 ;
	setAttr ".t";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" 0 0 90.000000000000028 ;
	setAttr ".r";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr ".s" -type "double3" 1.9526072098377265 4.7990393999195788 1.9526072098377265 ;
	setAttr ".s";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
lockNode -l 1 -lu 1;
createNode mesh -n "pCylinderShape1" -p "pCylinder1";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".iog[0].og[0]";
	setAttr ".iog[0].og[1]";
	setAttr ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".uvst";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".o";
	setAttr ".atm" no;
	setAttr ".vcs" 2;
lockNode -l 1 -lu 1;
createNode mesh -n "pCylinderShape1Orig" -p "pCylinder1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".uvst";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".o";
	setAttr ".atm" no;
lockNode -l 1 -lu 1;
createNode container -n "character_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 4 ".boc";
	setAttr -s 3 ".ish[1:3]" yes yes yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/20 15:29:17";
	setAttr ".aal" -type "attributeAlias" {"animationControlVisibility","borderConnections[0]"
		,"instance_1_activeModule","borderConnections[1]","instance_1_creationPoseWeight"
		,"borderConnections[2]","displayNoneBlueprintNodes","borderConnections[3]"} ;
lockNode -l 1 -lu 1;
createNode container -n "HingeJoint__instance_1:module_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 2 ".boc";
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/20 15:26:23";
	setAttr ".aal" -type "attributeAlias" {"activeModule","borderConnections[0]","creationPoseWeight"
		,"borderConnections[1]"} ;
lockNode -l 1 -lu 1;
createNode container -n "non_blueprint_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/20 15:29:17";
	setAttr ".aal" -type "attributeAlias" {"displayNoneBlueprintNodes","borderConnections[0]"
		} ;
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout3";
	setAttr ".ihi" 0;
	setAttr -s 3 ".hyp";
createNode container -n "HingeJoint__instance_1:blueprint_container";
	setAttr ".isc" yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/20 15:26:23";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout2";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode multiplyDivide -n "HingeJoint__instance_1:blueprint_hinge_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "HingeJoint__instance_1:blueprint_end_joint_original_Tx";
	setAttr ".i1" -type "float3" 4.1231055 0 0 ;
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "HingeJoint__instance_1:blueprint_hinge_joint_original_Tx";
	setAttr ".i1" -type "float3" 4.1231055 0 0 ;
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "HingeJoint__instance_1:blueprint_root_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode unitConversion -n "unitConversion1";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "HingeJoint__instance_1:blueprint_hinge_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "HingeJoint__instance_1:blueprint_root_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout1";
	setAttr ".ihi" 0;
	setAttr -s 18 ".hyp";
createNode unitConversion -n "unitConversion2";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "HingeJoint__instance_1:blueprint_end_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "HingeJoint__instance_1:blueprint_hinge_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode skinCluster -n "pCylinder1_skinCluster";
	setAttr ".ip";
	setAttr -s 120 ".wl";
	setAttr -s 2 ".wl[0].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[1].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[2].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[3].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[4].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[5].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[6].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[7].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[8].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[9].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[10].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[11].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[12].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[13].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[14].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[15].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[16].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[17].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[18].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[19].w[1:2]"  0.5 0.5;
	setAttr -s 2 ".wl[20].w[1:2]"  0.65470143972872452 0.34529856027127553;
	setAttr -s 2 ".wl[21].w[1:2]"  0.6964001330865206 0.3035998669134794;
	setAttr -s 2 ".wl[22].w[1:2]"  0.73343955589285226 0.26656044410714774;
	setAttr -s 2 ".wl[23].w[1:2]"  0.7589054312499165 0.24109456875008359;
	setAttr -s 2 ".wl[24].w[1:2]"  0.76795211416882603 0.23204788583117397;
	setAttr -s 2 ".wl[25].w[1:2]"  0.75890544512461133 0.24109455487538872;
	setAttr -s 2 ".wl[26].w[1:2]"  0.73343961044337136 0.2665603895566287;
	setAttr -s 2 ".wl[27].w[1:2]"  0.6964002215824926 0.3035997784175074;
	setAttr -s 2 ".wl[28].w[1:2]"  0.65470152312994156 0.34529847687005844;
	setAttr -s 2 ".wl[29].w[1:2]"  0.61510264914580193 0.38489735085419807;
	setAttr -s 2 ".wl[30].w[1:2]"  0.58221041055442391 0.41778958944557609;
	setAttr -s 2 ".wl[31].w[1:2]"  0.55790003632132956 0.44209996367867055;
	setAttr -s 2 ".wl[32].w[1:2]"  0.54196413548970634 0.45803586451029366;
	setAttr -s 2 ".wl[33].w[1:2]"  0.53320565622727478 0.46679434377272522;
	setAttr -s 2 ".wl[34].w[1:2]"  0.53044458039434916 0.46955541960565095;
	setAttr -s 2 ".wl[35].w[1:2]"  0.53320566403292236 0.46679433596707764;
	setAttr -s 2 ".wl[36].w[1:2]"  0.54196414717625851 0.45803585282374149;
	setAttr -s 2 ".wl[37].w[1:2]"  0.55790005768979656 0.44209994231020344;
	setAttr -s 2 ".wl[38].w[1:2]"  0.58221044944016498 0.41778955055983502;
	setAttr -s 2 ".wl[39].w[1:2]"  0.61510269531139106 0.384897304688609;
	setAttr -s 2 ".wl[40].w[1:2]"  0.92954131104466864 0.070458688955331417;
	setAttr -s 2 ".wl[41].w[1:2]"  0.95753668171976392 0.042463318280236084;
	setAttr -s 2 ".wl[42].w[1:2]"  0.97587077448963355 0.024129225510366524;
	setAttr -s 2 ".wl[43].w[1:2]"  0.98531577871963527 0.014684221280364685;
	setAttr -s 2 ".wl[44].w[1:2]"  0.98808885198870511 0.011911148011294963;
	setAttr -s 2 ".wl[45].w[1:2]"  0.98531578230860117 0.014684217691398833;
	setAttr -s 2 ".wl[46].w[1:2]"  0.9758707941527851 0.024129205847214983;
	setAttr -s 2 ".wl[47].w[1:2]"  0.95753672923032107 0.04246327076967895;
	setAttr -s 2 ".wl[48].w[1:2]"  0.92954137688830751 0.07045862311169257;
	setAttr -s 2 ".wl[49].w[1:2]"  0.89427579374145771 0.10572420625854226;
	setAttr -s 2 ".wl[50].w[1:2]"  0.85671976615729384 0.14328023384270616;
	setAttr -s 2 ".wl[51].w[1:2]"  0.82235615261901485 0.17764384738098518;
	setAttr -s 2 ".wl[52].w[1:2]"  0.79544375426917613 0.2045562457308239;
	setAttr -s 2 ".wl[53].w[1:2]"  0.77852369610155736 0.22147630389844269;
	setAttr -s 2 ".wl[54].w[1:2]"  0.77277604599937078 0.22722395400062925;
	setAttr -s 2 ".wl[55].w[1:2]"  0.77852371843361656 0.22147628156638341;
	setAttr -s 2 ".wl[56].w[1:2]"  0.79544378392211157 0.20455621607788851;
	setAttr -s 2 ".wl[57].w[1:2]"  0.822356196353074 0.17764380364692597;
	setAttr -s 2 ".wl[58].w[1:2]"  0.85671982601671792 0.14328017398328208;
	setAttr -s 2 ".wl[59].w[1:2]"  0.89427584575430885 0.10572415424569109;
	setAttr -s 2 ".wl[60].w[0:1]"  0.6138057591787015 0.38619424082129844;
	setAttr -s 2 ".wl[61].w[0:1]"  0.61220046892073521 0.38779953107926479;
	setAttr -s 2 ".wl[62].w[0:1]"  0.61600035842571366 0.38399964157428645;
	setAttr -s 2 ".wl[63].w[0:1]"  0.6240230899246989 0.37597691007530104;
	setAttr -s 2 ".wl[64].w[0:1]"  0.62879179510027072 0.37120820489972933;
	setAttr -s 2 ".wl[65].w[0:1]"  0.62402311608619321 0.3759768839138069;
	setAttr -s 2 ".wl[66].w[0:1]"  0.61600043697927243 0.38399956302072752;
	setAttr -s 2 ".wl[67].w[0:1]"  0.61220056580210591 0.38779943419789409;
	setAttr -s 2 ".wl[68].w[0:1]"  0.61380584174323205 0.38619415825676795;
	setAttr -s 2 ".wl[69].w[0:1]"  0.61922715586548627 0.38077284413451368;
	setAttr -s 2 ".wl[70].w[0:1]"  0.62655268286637522 0.37344731713362478;
	setAttr -s 2 ".wl[71].w[0:1]"  0.63411020811778118 0.36588979188221887;
	setAttr -s 2 ".wl[72].w[0:1]"  0.64053969691832813 0.35946030308167198;
	setAttr -s 2 ".wl[73].w[0:1]"  0.64482233889403939 0.35517766110596055;
	setAttr -s 2 ".wl[74].w[0:1]"  0.6463221273430575 0.35367787265694256;
	setAttr -s 2 ".wl[75].w[0:1]"  0.64482234806942806 0.35517765193057194;
	setAttr -s 2 ".wl[76].w[0:1]"  0.64053971104121898 0.35946028895878102;
	setAttr -s 2 ".wl[77].w[0:1]"  0.63411023194451166 0.36588976805548834;
	setAttr -s 2 ".wl[78].w[0:1]"  0.62655271933234125 0.3734472806676587;
	setAttr -s 2 ".wl[79].w[0:1]"  0.61922719806927207 0.38077280193072799;
	setAttr -s 2 ".wl[80].w[0:1]"  0.91305029037597996 0.086949709624020016;
	setAttr -s 2 ".wl[81].w[0:1]"  0.91438656583215605 0.085613434167844005;
	setAttr -s 2 ".wl[82].w[0:1]"  0.91698259959072015 0.083017400409279948;
	setAttr -s 2 ".wl[83].w[0:1]"  0.91954246155315744 0.080457538446842627;
	setAttr -s 2 ".wl[84].w[0:1]"  0.9206112371800298 0.079388762819970232;
	setAttr -s 2 ".wl[85].w[0:1]"  0.91954247732712502 0.08045752267287494;
	setAttr -s 2 ".wl[86].w[0:1]"  0.91698265778820731 0.083017342211792758;
	setAttr -s 2 ".wl[87].w[0:1]"  0.91438665475473135 0.085613345245268646;
	setAttr -s 2 ".wl[88].w[0:1]"  0.91305037944701439 0.086949620552985621;
	setAttr -s 2 ".wl[89].w[0:1]"  0.91348901354771495 0.086510986452285055;
	setAttr -s 2 ".wl[90].w[0:1]"  0.91542913943889292 0.084570860561107117;
	setAttr -s 2 ".wl[91].w[0:1]"  0.91814021466953388 0.081859785330466089;
	setAttr -s 2 ".wl[92].w[0:1]"  0.92078832720313686 0.079211672796863128;
	setAttr -s 2 ".wl[93].w[0:1]"  0.9226747798304511 0.077325220169548861;
	setAttr -s 2 ".wl[94].w[0:1]"  0.92335400102670617 0.076645998973293814;
	setAttr -s 2 ".wl[95].w[0:1]"  0.92267479276014652 0.077325207239853505;
	setAttr -s 2 ".wl[96].w[0:1]"  0.92078834647609564 0.07921165352390433;
	setAttr -s 2 ".wl[97].w[0:1]"  0.91814024635406299 0.08185975364593695;
	setAttr -s 2 ".wl[98].w[0:1]"  0.91542918673877716 0.084570813261222941;
	setAttr -s 2 ".wl[99].w[0:1]"  0.91348906459013068 0.086510935409869344;
	setAttr -s 2 ".wl[100].w[0:1]"  0.97276761163589853 0.027232388364101457;
	setAttr -s 2 ".wl[101].w[0:1]"  0.97039760349220117 0.029602396507798872;
	setAttr -s 2 ".wl[102].w[0:1]"  0.96829196789293148 0.031708032107068566;
	setAttr -s 2 ".wl[103].w[0:1]"  0.96682081245282603 0.033179187547173951;
	setAttr -s 2 ".wl[104].w[0:1]"  0.96629038017714419 0.033709619822855801;
	setAttr -s 2 ".wl[105].w[0:1]"  0.9668208183054644 0.033179181694535605;
	setAttr -s 2 ".wl[106].w[0:1]"  0.96829198868766098 0.031708011312339093;
	setAttr -s 2 ".wl[107].w[0:1]"  0.97039763399720569 0.029602366002794363;
	setAttr -s 2 ".wl[108].w[0:1]"  0.97276764185261921 0.027232358147380762;
	setAttr -s 2 ".wl[109].w[0:1]"  0.97507942739441211 0.024920572605587943;
	setAttr -s 2 ".wl[110].w[0:1]"  0.97711097610346886 0.022889023896531122;
	setAttr -s 2 ".wl[111].w[0:1]"  0.97873928041018921 0.021260719589810764;
	setAttr -s 2 ".wl[112].w[0:1]"  0.97991175883924875 0.020088241160751346;
	setAttr -s 2 ".wl[113].w[0:1]"  0.98061446073056158 0.019385539269438385;
	setAttr -s 2 ".wl[114].w[0:1]"  0.98084812913318908 0.019151870866810961;
	setAttr -s 2 ".wl[115].w[0:1]"  0.98061446529122875 0.019385534708771246;
	setAttr -s 2 ".wl[116].w[0:1]"  0.97991176555806403 0.020088234441936009;
	setAttr -s 2 ".wl[117].w[0:1]"  0.97873929130109971 0.021260708698900337;
	setAttr -s 2 ".wl[118].w[0:1]"  0.97711099207973362 0.022889007920266349;
	setAttr -s 2 ".wl[119].w[0:1]"  0.97507944452423645 0.02492055547576353;
	setAttr ".wl";
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 0.97014173978704799 8.4466777113566339e-010 -0.24253866644920688 -0
		 1.0339757656912844e-025 -1 -3.4826107667766688e-009 0 -0.24253866644920688 3.378626068281823e-009 -0.97014173978704776 -0
		 -0 0 0 1;
	setAttr ".pm[1]" -type "matrix" 0.97014173978704765 8.4466777113566339e-010 0.24253866644920799 -0
		 1.6388949220632042e-009 -1 -3.072881577168932e-009 0 0.24253866644920788 3.378626068281823e-009 -0.97014173978704754 -0
		 -3.6380221218935098 0 -1.94030776396467 1;
	setAttr ".pm[2]" -type "matrix" 0.97014173978704765 8.4466777113566339e-010 0.24253866644920799 -0
		 1.6388949220632042e-009 -1 -3.072881577168932e-009 0 0.24253866644920788 3.378626068281823e-009 -0.97014173978704754 -0
		 -7.7611276478639688 8.2718061255302749e-025 -1.9403077639646711 1;
	setAttr ".pm";
	setAttr ".gm" -type "matrix" -8.6713179296437138e-016 1.9526072098377265 0 0 -4.7990393999195788 -2.1312016151496044e-015 0 0
		 0 0 1.9526072098377265 0 4.0774678903275481 1.8107594936045626e-015 0 1;
	setAttr -s 3 ".ma";
	setAttr ".ma";
	setAttr -s 3 ".dpf[0:2]"  4 4 4;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
lockNode -l 1 -lu 1;
createNode objectSet -n "tweakSet1";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".vo" yes;
lockNode -l 1 -lu 1;
createNode objectSet -n "pCylinder1_skinClusterSet";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".vo" yes;
lockNode -l 1 -lu 1;
createNode deleteComponent -n "deleteComponent1";
	setAttr ".dc" -type "componentList" 1 "f[100:101]";
lockNode -l 1 -lu 1;
createNode reverse -n "reverse_moduleMaintenanceVisibility";
	setAttr ".i";
lockNode -l 1 -lu 1;
createNode tweak -n "tweak1";
	setAttr ".ip";
	setAttr ".vl";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout4";
	setAttr ".ihi" 0;
	setAttr -s 16 ".hyp";
createNode groupParts -n "pCylinder1_skinClusterGroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
lockNode -l 1 -lu 1;
createNode polyCylinder -n "polyCylinder1";
	setAttr ".sh" 5;
	setAttr ".cuv" 3;
lockNode -l 1 -lu 1;
createNode groupId -n "pCylinder1_skinClusterGroupId";
	setAttr ".ihi" 0;
lockNode -l 1 -lu 1;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
lockNode -l 1 -lu 1;
createNode groupId -n "groupId2";
	setAttr ".ihi" 0;
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "non_blueprint_visibilityMultiply";
	setAttr ".i1";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode dagPose -n "bindPose1";
	setAttr -s 6 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 6 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0.99250736515832672 2.1276108389405262e-010 -0.12218481946001312 1.7282584180027662e-009 1
		 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.123105525970459 0 5.5511151231257827e-016 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.24253866644920744 0 0.97014173978704787 1
		 1 1 no;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.123105525970459 3.4578755056242158e-025
		 8.8817841970012523e-016 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr -s 6 ".m";
	setAttr -s 6 ".p";
	setAttr -s 6 ".g[0:5]" yes yes yes no no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 11 ".u";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 18 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surfaces" "Particles" "Fluids" "Image Planes" "UI:" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 0 0 0 0 0 0 0 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "HingeJoint__instance_1:HOOK_IN.sy" "HingeJoint__instance_1:module_grp.hierarchicalScale"
		 -l on;
connectAttr "character_grp.moduleMaintenanceVisibility" "HingeJoint__instance_1:blueprint_joints_grp.v"
		 -l on;
connectAttr "unitConversion1.o" "HingeJoint__instance_1:blueprint_root_joint.r" 
		-l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint.s" "HingeJoint__instance_1:blueprint_hinge_joint.is"
		 -l on;
connectAttr "unitConversion2.o" "HingeJoint__instance_1:blueprint_hinge_joint.r"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addTx.o1" "HingeJoint__instance_1:blueprint_hinge_joint.tx"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.s" "HingeJoint__instance_1:blueprint_end_joint.is"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_addTx.o1" "HingeJoint__instance_1:blueprint_end_joint.tx"
		 -l on;
connectAttr "HingeJoint__instance_1:creationPose_root_joint.s" "HingeJoint__instance_1:creationPose_hinge_joint.is"
		 -l on;
connectAttr "HingeJoint__instance_1:creationPose_hinge_joint.s" "HingeJoint__instance_1:creationPose_end_joint.is"
		 -l on;
connectAttr "non_blueprint_visibilityMultiply.ox" "non_blueprint_grp.v" -l on;
connectAttr "pCylinder1_skinClusterGroupId.id" "pCylinderShape1.iog.og[0].gid" -l
		 on;
connectAttr "pCylinder1_skinClusterSet.mwc" "pCylinderShape1.iog.og[0].gco" -l on
		;
connectAttr "groupId2.id" "pCylinderShape1.iog.og[1].gid" -l on;
connectAttr "tweakSet1.mwc" "pCylinderShape1.iog.og[1].gco" -l on;
connectAttr "pCylinder1_skinCluster.og[0]" "pCylinderShape1.i" -l on;
connectAttr "tweak1.vl[0].vt[0]" "pCylinderShape1.twl" -l on;
connectAttr "deleteComponent1.og" "pCylinderShape1Orig.i" -l on;
connectAttr "character_grp.animationControlVisibility" "character_container.boc[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:module_container.boc[0]" "character_container.boc[1]"
		 -l on;
connectAttr "HingeJoint__instance_1:module_container.boc[1]" "character_container.boc[2]"
		 -l on;
connectAttr "non_blueprint_container.boc[0]" "character_container.boc[3]" -l on;
connectAttr "hyperLayout3.msg" "character_container.hl" -l on;
connectAttr "HingeJoint__instance_1:SETTINGS.activeModule" "HingeJoint__instance_1:module_container.boc[0]"
		;
connectAttr "HingeJoint__instance_1:SETTINGS.creationPoseWeight" "HingeJoint__instance_1:module_container.boc[1]"
		;
connectAttr "hyperLayout2.msg" "HingeJoint__instance_1:module_container.hl" -l on
		;
connectAttr "non_blueprint_grp.display" "non_blueprint_container.boc[0]";
connectAttr "hyperLayout4.msg" "non_blueprint_container.hl" -l on;
connectAttr "HingeJoint__instance_1:module_container.msg" "hyperLayout3.hyp[0].dn"
		;
connectAttr "character_grp.msg" "hyperLayout3.hyp[1].dn";
connectAttr "non_blueprint_container.msg" "hyperLayout3.hyp[2].dn";
connectAttr "hyperLayout1.msg" "HingeJoint__instance_1:blueprint_container.hl" -l
		 on;
connectAttr "HingeJoint__instance_1:module_grp.msg" "hyperLayout2.hyp[0].dn";
connectAttr "HingeJoint__instance_1:HOOK_IN.msg" "hyperLayout2.hyp[1].dn";
connectAttr "HingeJoint__instance_1:SETTINGS.msg" "hyperLayout2.hyp[2].dn";
connectAttr "HingeJoint__instance_1:blueprint_container.msg" "hyperLayout2.hyp[3].dn"
		;
connectAttr "HingeJoint__instance_1:SETTINGSShape.msg" "hyperLayout2.hyp[4].dn";
connectAttr "HingeJoint__instance_1:SETTINGS.creationPoseWeight" "HingeJoint__instance_1:blueprint_end_joint_original_Tx.i2x"
		 -l on;
connectAttr "HingeJoint__instance_1:SETTINGS.creationPoseWeight" "HingeJoint__instance_1:blueprint_hinge_joint_original_Tx.i2x"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_addRotations.o3" "unitConversion1.i"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_dummyRotationsMultiply.o" "HingeJoint__instance_1:blueprint_hinge_joint_addRotations.i3[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_dummyRotationsMultiply.o" "HingeJoint__instance_1:blueprint_root_joint_addRotations.i3[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_addRotations.msg" "hyperLayout1.hyp[0].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[1].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addRotations.msg" "hyperLayout1.hyp[2].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[3].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addTx.msg" "hyperLayout1.hyp[4].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_original_Tx.msg" "hyperLayout1.hyp[5].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_addTx.msg" "hyperLayout1.hyp[6].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_original_Tx.msg" "hyperLayout1.hyp[7].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_joints_grp.msg" "hyperLayout1.hyp[8].dn"
		;
connectAttr "HingeJoint__instance_1:creationPose_joint_grp.msg" "hyperLayout1.hyp[9].dn"
		;
connectAttr "unitConversion1.msg" "hyperLayout1.hyp[10].dn";
connectAttr "unitConversion2.msg" "hyperLayout1.hyp[11].dn";
connectAttr "HingeJoint__instance_1:blueprint_root_joint.msg" "hyperLayout1.hyp[12].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.msg" "hyperLayout1.hyp[13].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_end_joint.msg" "hyperLayout1.hyp[14].dn"
		;
connectAttr "HingeJoint__instance_1:creationPose_root_joint.msg" "hyperLayout1.hyp[15].dn"
		;
connectAttr "HingeJoint__instance_1:creationPose_hinge_joint.msg" "hyperLayout1.hyp[16].dn"
		;
connectAttr "HingeJoint__instance_1:creationPose_end_joint.msg" "hyperLayout1.hyp[17].dn"
		;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addRotations.o3" "unitConversion2.i"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_original_Tx.ox" "HingeJoint__instance_1:blueprint_end_joint_addTx.i1[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_original_Tx.ox" "HingeJoint__instance_1:blueprint_hinge_joint_addTx.i1[0]"
		 -l on;
connectAttr "pCylinder1_skinClusterGroupParts.og" "pCylinder1_skinCluster.ip[0].ig"
		 -l on;
connectAttr "pCylinder1_skinClusterGroupId.id" "pCylinder1_skinCluster.ip[0].gi"
		 -l on;
connectAttr "bindPose1.msg" "pCylinder1_skinCluster.bp" -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint.wm" "pCylinder1_skinCluster.ma[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.wm" "pCylinder1_skinCluster.ma[1]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_end_joint.wm" "pCylinder1_skinCluster.ma[2]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint.liw" "pCylinder1_skinCluster.lw[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.liw" "pCylinder1_skinCluster.lw[1]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_end_joint.liw" "pCylinder1_skinCluster.lw[2]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_root_joint.obcc" "pCylinder1_skinCluster.ifcl[0]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.obcc" "pCylinder1_skinCluster.ifcl[1]"
		 -l on;
connectAttr "HingeJoint__instance_1:blueprint_end_joint.obcc" "pCylinder1_skinCluster.ifcl[2]"
		 -l on;
connectAttr "groupId2.msg" "tweakSet1.gn" -l on -na;
connectAttr "pCylinderShape1.iog.og[1]" "tweakSet1.dsm" -l on -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]" -l on;
connectAttr "pCylinder1_skinClusterGroupId.msg" "pCylinder1_skinClusterSet.gn" -l
		 on -na;
connectAttr "pCylinderShape1.iog.og[0]" "pCylinder1_skinClusterSet.dsm" -l on -na
		;
connectAttr "pCylinder1_skinCluster.msg" "pCylinder1_skinClusterSet.ub[0]" -l on
		;
connectAttr "polyCylinder1.out" "deleteComponent1.ig" -l on;
connectAttr "character_grp.moduleMaintenanceVisibility" "reverse_moduleMaintenanceVisibility.ix"
		 -l on;
connectAttr "groupParts2.og" "tweak1.ip[0].ig" -l on;
connectAttr "groupId2.id" "tweak1.ip[0].gi" -l on;
connectAttr "non_blueprint_grp.msg" "hyperLayout4.hyp[0].dn";
connectAttr "pCylinder1.msg" "hyperLayout4.hyp[1].dn";
connectAttr "pCylinderShape1.msg" "hyperLayout4.hyp[2].dn";
connectAttr "pCylinderShape1Orig.msg" "hyperLayout4.hyp[3].dn";
connectAttr "pCylinder1_skinCluster.msg" "hyperLayout4.hyp[4].dn";
connectAttr "tweakSet1.msg" "hyperLayout4.hyp[5].dn";
connectAttr "pCylinder1_skinClusterSet.msg" "hyperLayout4.hyp[6].dn";
connectAttr "deleteComponent1.msg" "hyperLayout4.hyp[7].dn";
connectAttr "reverse_moduleMaintenanceVisibility.msg" "hyperLayout4.hyp[8].dn";
connectAttr "tweak1.msg" "hyperLayout4.hyp[9].dn";
connectAttr "pCylinder1_skinClusterGroupParts.msg" "hyperLayout4.hyp[10].dn";
connectAttr "polyCylinder1.msg" "hyperLayout4.hyp[11].dn";
connectAttr "pCylinder1_skinClusterGroupId.msg" "hyperLayout4.hyp[12].dn";
connectAttr "groupParts2.msg" "hyperLayout4.hyp[13].dn";
connectAttr "groupId2.msg" "hyperLayout4.hyp[14].dn";
connectAttr "non_blueprint_visibilityMultiply.msg" "hyperLayout4.hyp[15].dn";
connectAttr "tweak1.og[0]" "pCylinder1_skinClusterGroupParts.ig" -l on;
connectAttr "pCylinder1_skinClusterGroupId.id" "pCylinder1_skinClusterGroupParts.gi"
		 -l on;
connectAttr "pCylinderShape1Orig.w" "groupParts2.ig" -l on;
connectAttr "groupId2.id" "groupParts2.gi" -l on;
connectAttr "reverse_moduleMaintenanceVisibility.ox" "non_blueprint_visibilityMultiply.i1x"
		 -l on;
connectAttr "non_blueprint_grp.display" "non_blueprint_visibilityMultiply.i2x" -l
		 on;
connectAttr "HingeJoint__instance_1:module_grp.msg" "bindPose1.m[0]";
connectAttr "HingeJoint__instance_1:HOOK_IN.msg" "bindPose1.m[1]";
connectAttr "HingeJoint__instance_1:blueprint_joints_grp.msg" "bindPose1.m[2]";
connectAttr "HingeJoint__instance_1:blueprint_root_joint.msg" "bindPose1.m[3]";
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.msg" "bindPose1.m[4]";
connectAttr "HingeJoint__instance_1:blueprint_end_joint.msg" "bindPose1.m[5]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "bindPose1.m[2]" "bindPose1.p[3]";
connectAttr "bindPose1.m[3]" "bindPose1.p[4]";
connectAttr "bindPose1.m[4]" "bindPose1.p[5]";
connectAttr "HingeJoint__instance_1:blueprint_root_joint.bps" "bindPose1.wm[3]";
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint.bps" "bindPose1.wm[4]"
		;
connectAttr "HingeJoint__instance_1:blueprint_end_joint.bps" "bindPose1.wm[5]";
connectAttr "pCylinderShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_root_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_hinge_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "HingeJoint__instance_1:blueprint_end_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "reverse_moduleMaintenanceVisibility.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "non_blueprint_visibilityMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
// End of testing.ma
