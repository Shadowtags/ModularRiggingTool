//Maya ASCII 2014 scene
//Name: cube_spline.ma
//Last modified: Wed, Jul 22, 2015 12:59:44 PM
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
createNode transform -n "Spline__instance_1:module_grp" -p "character_grp";
	addAttr -ci true -sn "hierarchicalScale" -ln "hierarchicalScale" -at "float";
lockNode -l 1 -lu 1;
createNode transform -n "Spline__instance_1:HOOK_IN" -p "Spline__instance_1:module_grp";
	setAttr ".s";
	setAttr ".sy";
lockNode -l 1 -lu 1;
createNode transform -n "Spline__instance_1:blueprint_joints_grp" -p "Spline__instance_1:HOOK_IN";
	addAttr -ci true -sn "controlModulesInstalled" -ln "controlModulesInstalled" -min 
		0 -max 1 -at "bool";
	setAttr ".ove" yes;
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:blueprint_spline_1_joint" -p "Spline__instance_1:blueprint_joints_grp";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 180 0 90.000000000000014 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-016 1 0 0 1 2.2204460492503131e-016 1.2246467991473532e-016 0
		 1.2246467991473532e-016 2.4651903288156619e-032 -1 0 0 0 0 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:blueprint_spline_2_joint" -p "Spline__instance_1:blueprint_spline_1_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 3.75 8.326672684688678e-016 1.0197233050851688e-031 ;
	setAttr ".t";
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-016 1 0 0 1 2.2204460492503131e-016 1.2246467991473532e-016 0
		 1.2246467991473532e-016 2.4651903288156619e-032 -1 0 3.944304526105059e-031 3.75 0 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:blueprint_spline_3_joint" -p "Spline__instance_1:blueprint_spline_2_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 3.75 8.326672684688676e-016 9.8607613152626498e-032 ;
	setAttr ".t";
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-016 1 0 0 1 2.2204460492503131e-016 1.2246467991473532e-016 0
		 1.2246467991473532e-016 2.4651903288156619e-032 -1 0 5.9164567891575885e-031 7.5 3.3647173558903631e-033 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:blueprint_spline_4_joint" -p "Spline__instance_1:blueprint_spline_3_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 3.75 8.326672684688676e-016 9.8607613152626476e-032 ;
	setAttr ".t";
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-016 1 0 0 1 2.2204460492503131e-016 1.2246467991473532e-016 0
		 1.2246467991473532e-016 2.4651903288156619e-032 -1 0 7.8886090522101181e-031 11.25 6.729434711780748e-033 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:blueprint_spline_5_joint" -p "Spline__instance_1:blueprint_spline_4_joint";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".obcc";
	setAttr ".t" -type "double3" 3.75 8.326672684688678e-016 9.8607613152626563e-032 ;
	setAttr ".t";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 180 0 90.000000000000014 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 1.2246467991473532e-016 0 1.4997597826618576e-032 1 -1.224646799147353e-016 0
		 -1.2246467991473532e-016 1.224646799147353e-016 1 0 1.1832913578315177e-030 15 1.0094152067671067e-032 1;
	setAttr ".liw";
lockNode -l 1 -lu 1;
createNode transform -n "Spline__instance_1:creationPose_joints_grp" -p "Spline__instance_1:HOOK_IN";
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:creationPose_spline_1_joint" -p "Spline__instance_1:creationPose_joints_grp";
	setAttr ".v" no;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 180 0 90.000000000000014 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:creationPose_spline_2_joint" -p "Spline__instance_1:creationPose_spline_1_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.7500000000000009 8.326672684688678e-016 1.0197233050851688e-031 ;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:creationPose_spline_3_joint" -p "Spline__instance_1:creationPose_spline_2_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.7500000000000009 8.326672684688676e-016 9.8607613152626498e-032 ;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:creationPose_spline_4_joint" -p "Spline__instance_1:creationPose_spline_3_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.7500000000000018 8.326672684688676e-016 9.8607613152626476e-032 ;
	setAttr ".s";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode joint -n "Spline__instance_1:creationPose_spline_5_joint" -p "Spline__instance_1:creationPose_spline_4_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.75 8.326672684688678e-016 9.8607613152626563e-032 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 180 0 90.000000000000014 ;
	setAttr ".ssc" no;
lockNode -l 1 -lu 1;
createNode transform -n "Spline__instance_1:SETTINGS" -p "Spline__instance_1:module_grp";
	addAttr -ci true -sn "activeModule" -ln "activeModule" -min 0 -max 0 -en "None" 
		-at "enum";
	addAttr -ci true -sn "creationPoseWeight" -ln "creationPoseWeight" -dv 1 -at "float";
	setAttr ".v" no;
lockNode -l 1 -lu 1;
createNode locator -n "Spline__instance_1:SETTINGSShape" -p "Spline__instance_1:SETTINGS";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode transform -n "non_blueprint_grp" -p "character_grp";
	addAttr -ci true -k true -sn "display" -ln "display" -dv 1 -min 0 -max 1 -at "bool";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".rp" -type "double3" 0 7.8470618067054954 0 ;
	setAttr ".sp" -type "double3" 0 7.8470618067054954 0 ;
	setAttr -k on ".display";
lockNode -l 1 -lu 1;
createNode transform -n "pCube1" -p "non_blueprint_grp";
	setAttr ".t" -type "double3" 0 7.8470618067054954 0 ;
	setAttr ".t";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr ".r";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr ".s" -type "double3" 3.2609279055536011 15.743482334310869 3.2609279055536011 ;
	setAttr ".s";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
lockNode -l 1 -lu 1;
createNode mesh -n "pCubeShape1" -p "pCube1";
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
createNode mesh -n "pCubeShape1Orig" -p "pCube1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 56 ".uvst[0].uvsp[0:55]" -type "float2" 0.375 0 0.625 0 0.375
		 0.03125 0.625 0.03125 0.375 0.0625 0.625 0.0625 0.375 0.09375 0.625 0.09375 0.375
		 0.125 0.625 0.125 0.375 0.15625 0.625 0.15625 0.375 0.1875 0.625 0.1875 0.375 0.21875
		 0.625 0.21875 0.375 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.53125 0.625 0.53125
		 0.375 0.5625 0.625 0.5625 0.375 0.59375 0.625 0.59375 0.375 0.625 0.625 0.625 0.375
		 0.65625 0.625 0.65625 0.375 0.6875 0.625 0.6875 0.375 0.71875 0.625 0.71875 0.375
		 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0 0.875 0.03125 0.875 0.0625 0.875 0.09375
		 0.875 0.125 0.875 0.15625 0.875 0.1875 0.875 0.21875 0.875 0.25 0.125 0 0.125 0.03125
		 0.125 0.0625 0.125 0.09375 0.125 0.125 0.125 0.15625 0.125 0.1875 0.125 0.21875 0.125
		 0.25;
	setAttr ".uvst";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".o";
	setAttr ".ci";
	setAttr -s 36 ".vt[0:35]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 -0.375 0.5
		 0.5 -0.375 0.5 -0.5 -0.25 0.5 0.5 -0.25 0.5 -0.5 -0.125 0.5 0.5 -0.125 0.5 -0.5 0 0.5
		 0.5 0 0.5 -0.5 0.125 0.5 0.5 0.125 0.5 -0.5 0.25 0.5 0.5 0.25 0.5 -0.5 0.375 0.5
		 0.5 0.375 0.5 -0.5 0.5 0.5 0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 0.375 -0.5
		 0.5 0.375 -0.5 -0.5 0.25 -0.5 0.5 0.25 -0.5 -0.5 0.125 -0.5 0.5 0.125 -0.5 -0.5 0 -0.5
		 0.5 0 -0.5 -0.5 -0.125 -0.5 0.5 -0.125 -0.5 -0.5 -0.25 -0.5 0.5 -0.25 -0.5 -0.5 -0.375 -0.5
		 0.5 -0.375 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 68 ".ed[0:67]"  0 1 0 2 3 1 4 5 1 6 7 1 8 9 1 10 11 1 12 13 1
		 14 15 1 16 17 0 18 19 0 20 21 1 22 23 1 24 25 1 26 27 1 28 29 1 30 31 1 32 33 1 34 35 0
		 0 2 0 1 3 0 2 4 0 3 5 0 4 6 0 5 7 0 6 8 0 7 9 0 8 10 0 9 11 0 10 12 0 11 13 0 12 14 0
		 13 15 0 14 16 0 15 17 0 16 18 0 17 19 0 18 20 0 19 21 0 20 22 0 21 23 0 22 24 0 23 25 0
		 24 26 0 25 27 0 26 28 0 27 29 0 28 30 0 29 31 0 30 32 0 31 33 0 32 34 0 33 35 0 34 0 0
		 35 1 0 33 3 1 31 5 1 29 7 1 27 9 1 25 11 1 23 13 1 21 15 1 32 2 1 30 4 1 28 6 1 26 8 1
		 24 10 1 22 12 1 20 14 1;
	setAttr -s 34 -ch 136 ".fc[0:33]" -type "polyFaces" 
		f 4 0 19 -2 -19
		mu 0 4 0 1 3 2
		f 4 1 21 -3 -21
		mu 0 4 2 3 5 4
		f 4 2 23 -4 -23
		mu 0 4 4 5 7 6
		f 4 3 25 -5 -25
		mu 0 4 6 7 9 8
		f 4 4 27 -6 -27
		mu 0 4 8 9 11 10
		f 4 5 29 -7 -29
		mu 0 4 10 11 13 12
		f 4 6 31 -8 -31
		mu 0 4 12 13 15 14
		f 4 7 33 -9 -33
		mu 0 4 14 15 17 16
		f 4 8 35 -10 -35
		mu 0 4 16 17 19 18
		f 4 9 37 -11 -37
		mu 0 4 18 19 21 20
		f 4 10 39 -12 -39
		mu 0 4 20 21 23 22
		f 4 11 41 -13 -41
		mu 0 4 22 23 25 24
		f 4 12 43 -14 -43
		mu 0 4 24 25 27 26
		f 4 13 45 -15 -45
		mu 0 4 26 27 29 28
		f 4 14 47 -16 -47
		mu 0 4 28 29 31 30
		f 4 15 49 -17 -49
		mu 0 4 30 31 33 32
		f 4 16 51 -18 -51
		mu 0 4 32 33 35 34
		f 4 17 53 -1 -53
		mu 0 4 34 35 37 36
		f 4 -54 -52 54 -20
		mu 0 4 1 38 39 3
		f 4 -55 -50 55 -22
		mu 0 4 3 39 40 5
		f 4 -56 -48 56 -24
		mu 0 4 5 40 41 7
		f 4 -57 -46 57 -26
		mu 0 4 7 41 42 9
		f 4 -58 -44 58 -28
		mu 0 4 9 42 43 11
		f 4 -59 -42 59 -30
		mu 0 4 11 43 44 13
		f 4 -60 -40 60 -32
		mu 0 4 13 44 45 15
		f 4 -61 -38 -36 -34
		mu 0 4 15 45 46 17
		f 4 52 18 -62 50
		mu 0 4 47 0 2 48
		f 4 61 20 -63 48
		mu 0 4 48 2 4 49
		f 4 62 22 -64 46
		mu 0 4 49 4 6 50
		f 4 63 24 -65 44
		mu 0 4 50 6 8 51
		f 4 64 26 -66 42
		mu 0 4 51 8 10 52
		f 4 65 28 -67 40
		mu 0 4 52 10 12 53
		f 4 66 30 -68 38
		mu 0 4 53 12 14 54
		f 4 67 32 34 36
		mu 0 4 54 14 16 55;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".atm" no;
lockNode -l 1 -lu 1;
createNode container -n "character_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 4 ".boc";
	setAttr -s 3 ".ish[1:3]" yes yes yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/22 12:59:44";
	setAttr ".aal" -type "attributeAlias" {"animationControlVisibility","borderConnections[0]"
		,"instance_1_activeModule","borderConnections[1]","instance_1_creationPoseWeight"
		,"borderConnections[2]","displayNonBlueprintNodes","borderConnections[3]"} ;
lockNode -l 1 -lu 1;
createNode container -n "Spline__instance_1:module_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 2 ".boc";
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/22 12:58:59";
	setAttr ".aal" -type "attributeAlias" {"activeModule","borderConnections[0]","creationPoseWeight"
		,"borderConnections[1]"} ;
lockNode -l 1 -lu 1;
createNode container -n "non_blueprint_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/22 12:59:44";
	setAttr ".aal" -type "attributeAlias" {"displayNonBlueprintNodes","borderConnections[0]"
		} ;
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "moduleVisibilityMultiply";
	setAttr ".i1";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout3";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode reverse -n "reverse_moduleMaintenanceVisibility";
	setAttr ".i";
lockNode -l 1 -lu 1;
createNode container -n "Spline__instance_1:blueprint_container";
	setAttr ".isc" yes;
	setAttr ".ctor" -type "string" "Niklas";
	setAttr ".cdat" -type "string" "2015/07/22 12:58:59";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout2";
	setAttr ".ihi" 0;
	setAttr -s 5 ".hyp";
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_2_joint_original_Tx";
	setAttr ".i1" -type "float3" 3.75 0 0 ;
	setAttr ".i1";
	setAttr -l on ".i1x";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_5_joint_original_Tx";
	setAttr ".i1" -type "float3" 3.75 0 0 ;
	setAttr ".i1";
	setAttr -l on ".i1x";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_1_joint_original_Scale";
	setAttr ".i1" -type "float3" 1 1 1 ;
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_3_joint_original_Tx";
	setAttr ".i1" -type "float3" 3.75 0 0 ;
	setAttr ".i1";
	setAttr -l on ".i1x";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_2_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_4_joint_original_Tx";
	setAttr ".i1" -type "float3" 3.75 0 0 ;
	setAttr ".i1";
	setAttr -l on ".i1x";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_1_joint_original_Translate";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_3_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_4_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_1_joint_addTranslate";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode unitConversion -n "unitConversion1";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_1_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "Spline__instance_1:blueprint_spline_1_joint_dummyRotationsMultiply";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_1_joint_addScale";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_2_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode unitConversion -n "unitConversion2";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_2_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_3_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode unitConversion -n "unitConversion3";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_3_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_4_joint_addRotations";
	setAttr ".i3";
	setAttr ".i3";
lockNode -l 1 -lu 1;
createNode unitConversion -n "unitConversion4";
	setAttr ".cf" 0.017453292519943295;
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_4_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode plusMinusAverage -n "Spline__instance_1:blueprint_spline_5_joint_addTx";
	setAttr ".i1";
	setAttr ".i1";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout1";
	setAttr ".ihi" 0;
	setAttr -s 36 ".hyp";
createNode objectSet -n "pCube1_skinClusterSet";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".vo" yes;
lockNode -l 1 -lu 1;
createNode skinCluster -n "pCube1_skinCluster";
	setAttr ".ip";
	setAttr -s 36 ".wl";
	setAttr -s 2 ".wl[0].w[0:1]"  0.93121507477602661 0.068784925223973351;
	setAttr -s 2 ".wl[1].w[0:1]"  0.93121507477602661 0.068784925223973351;
	setAttr -s 2 ".wl[2].w[0:1]"  0.72259752677827305 0.27740247322172701;
	setAttr -s 2 ".wl[3].w[0:1]"  0.72259752677827305 0.27740247322172701;
	setAttr -s 2 ".wl[4].w[1:2]"  0.92133981964456646 0.078660180355433568;
	setAttr -s 2 ".wl[5].w[1:2]"  0.92133981964456646 0.078660180355433568;
	setAttr -s 2 ".wl[6].w[1:2]"  0.69063618994901521 0.30936381005098479;
	setAttr -s 2 ".wl[7].w[1:2]"  0.69063618994901521 0.30936381005098479;
	setAttr -s 2 ".wl[8].w[2:3]"  0.9099067883487989 0.090093211651201113;
	setAttr -s 2 ".wl[9].w[2:3]"  0.9099067883487989 0.090093211651201113;
	setAttr -s 2 ".wl[10].w[2:3]"  0.65807468777499523 0.34192531222500472;
	setAttr -s 2 ".wl[11].w[2:3]"  0.65807468777499523 0.34192531222500472;
	setAttr -s 2 ".wl[12].w[3:4]"  0.89671790845856125 0.1032820915414388;
	setAttr -s 2 ".wl[13].w[3:4]"  0.89671790845856125 0.1032820915414388;
	setAttr -s 2 ".wl[14].w[3:4]"  0.62589775210758003 0.37410224789241991;
	setAttr -s 2 ".wl[15].w[3:4]"  0.62589775210758003 0.37410224789241991;
	setAttr -s 2 ".wl[16].w[3:4]"  0.5 0.5;
	setAttr -s 2 ".wl[17].w[3:4]"  0.5 0.5;
	setAttr -s 2 ".wl[18].w[3:4]"  0.5 0.5;
	setAttr -s 2 ".wl[19].w[3:4]"  0.5 0.5;
	setAttr -s 2 ".wl[20].w[3:4]"  0.62589775210758003 0.37410224789241991;
	setAttr -s 2 ".wl[21].w[3:4]"  0.62589775210758003 0.37410224789241991;
	setAttr -s 2 ".wl[22].w[3:4]"  0.89671790845856125 0.1032820915414388;
	setAttr -s 2 ".wl[23].w[3:4]"  0.89671790845856125 0.1032820915414388;
	setAttr -s 2 ".wl[24].w[2:3]"  0.65807468777499523 0.34192531222500472;
	setAttr -s 2 ".wl[25].w[2:3]"  0.65807468777499523 0.34192531222500472;
	setAttr -s 2 ".wl[26].w[2:3]"  0.9099067883487989 0.090093211651201113;
	setAttr -s 2 ".wl[27].w[2:3]"  0.9099067883487989 0.090093211651201113;
	setAttr -s 2 ".wl[28].w[1:2]"  0.69063618994901521 0.30936381005098479;
	setAttr -s 2 ".wl[29].w[1:2]"  0.69063618994901521 0.30936381005098479;
	setAttr -s 2 ".wl[30].w[1:2]"  0.92133981964456646 0.078660180355433568;
	setAttr -s 2 ".wl[31].w[1:2]"  0.92133981964456646 0.078660180355433568;
	setAttr -s 2 ".wl[32].w[0:1]"  0.72259752677827305 0.27740247322172701;
	setAttr -s 2 ".wl[33].w[0:1]"  0.72259752677827305 0.27740247322172701;
	setAttr -s 2 ".wl[34].w[0:1]"  0.93121507477602661 0.068784925223973351;
	setAttr -s 2 ".wl[35].w[0:1]"  0.93121507477602661 0.068784925223973351;
	setAttr ".wl";
	setAttr -s 5 ".pm";
	setAttr ".pm[0]" -type "matrix" -2.2204460492503131e-016 1 1.2246467991473532e-016 -0
		 1 2.2204460492503131e-016 2.7192621468937821e-032 -0 -2.5407181807812022e-033 1.2246467991473532e-016 -1 0
		 -0 0 -0 1;
	setAttr ".pm[1]" -type "matrix" -2.2204460492503131e-016 1 1.2246467991473532e-016 -0
		 1 2.2204460492503131e-016 2.7192621468937821e-032 -0 -2.5407181807812022e-033 1.2246467991473532e-016 -1 0
		 -3.75 -8.326672684688678e-016 -1.0197233050851688e-031 1;
	setAttr ".pm[2]" -type "matrix" -2.2204460492503131e-016 1 1.2246467991473532e-016 -0
		 1 2.2204460492503131e-016 2.7192621468937821e-032 -0 -2.5407181807812022e-033 1.2246467991473532e-016 -1 0
		 -7.5 -1.6653345369377354e-015 -2.0057994366114338e-031 1;
	setAttr ".pm[3]" -type "matrix" -2.2204460492503131e-016 1 1.2246467991473532e-016 -0
		 1 2.2204460492503131e-016 2.7192621468937821e-032 -0 -2.5407181807812022e-033 1.2246467991473532e-016 -1 0
		 -11.25 -2.498001805406603e-015 -2.9918755681376986e-031 1;
	setAttr ".pm[4]" -type "matrix" 1 1.4997597826618573e-032 -1.2246467991473532e-016 -0
		 -2.7369110631344083e-048 1 1.224646799147353e-016 0 1.2246467991473532e-016 -1.224646799147353e-016 1 -0
		 -1.1832913578315177e-030 -15 -1.8369701987210296e-015 1;
	setAttr ".pm";
	setAttr ".gm" -type "matrix" 3.2609279055536011 0 0 0 0 15.743482334310869 0 0 0 0 3.2609279055536011 0
		 0 7.8470618067054954 0 1;
	setAttr -s 5 ".ma";
	setAttr ".ma";
	setAttr -s 5 ".dpf[0:4]"  4 4 4 4 4;
	setAttr -s 5 ".lw";
	setAttr -s 5 ".lw";
	setAttr ".ucm" yes;
	setAttr -s 5 ".ifcl";
	setAttr -s 5 ".ifcl";
lockNode -l 1 -lu 1;
createNode objectSet -n "tweakSet1";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".vo" yes;
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "non_blueprint_visibilityMultiply";
	setAttr ".i1";
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode tweak -n "tweak1";
	setAttr ".ip";
	setAttr ".vl";
lockNode -l 1 -lu 1;
createNode groupId -n "pCube1_skinClusterGroupId";
	setAttr ".ihi" 0;
lockNode -l 1 -lu 1;
createNode groupParts -n "pCube1_skinClusterGroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
lockNode -l 1 -lu 1;
createNode groupId -n "groupId2";
	setAttr ".ihi" 0;
lockNode -l 1 -lu 1;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout4";
	setAttr ".ihi" 0;
	setAttr -s 13 ".hyp";
createNode dagPose -n "bindPose1";
	setAttr -s 8 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0.70710678118654746 0.70710678118654757 4.329780281177467e-017 4.3297802811774658e-017 1
		 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.75 8.326672684688678e-016
		 1.0197233050851688e-031 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.75 8.326672684688676e-016
		 9.8607613152626498e-032 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.75 8.326672684688676e-016
		 9.8607613152626476e-032 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.75 8.326672684688678e-016
		 9.8607613152626563e-032 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.70710678118654746 0.70710678118654757 4.329780281177467e-017 4.3297802811774658e-017 1
		 1 1 no;
	setAttr -s 8 ".m";
	setAttr -s 8 ".p";
	setAttr -s 8 ".g[0:7]" yes yes yes no no no no no;
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
	setAttr -s 23 ".u";
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
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "Spline__instance_1:HOOK_IN.sy" "Spline__instance_1:module_grp.hierarchicalScale"
		 -l on;
connectAttr "character_grp.moduleMaintenanceVisibility" "Spline__instance_1:blueprint_joints_grp.v"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addScale.o3" "Spline__instance_1:blueprint_spline_1_joint.s"
		 -l on;
connectAttr "unitConversion1.o" "Spline__instance_1:blueprint_spline_1_joint.r" 
		-l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addTranslate.o3" "Spline__instance_1:blueprint_spline_1_joint.t"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint.s" "Spline__instance_1:blueprint_spline_2_joint.is"
		 -l on;
connectAttr "unitConversion2.o" "Spline__instance_1:blueprint_spline_2_joint.r" 
		-l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addTx.o1" "Spline__instance_1:blueprint_spline_2_joint.tx"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint.s" "Spline__instance_1:blueprint_spline_3_joint.is"
		 -l on;
connectAttr "unitConversion3.o" "Spline__instance_1:blueprint_spline_3_joint.r" 
		-l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addTx.o1" "Spline__instance_1:blueprint_spline_3_joint.tx"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint.s" "Spline__instance_1:blueprint_spline_4_joint.is"
		 -l on;
connectAttr "unitConversion4.o" "Spline__instance_1:blueprint_spline_4_joint.r" 
		-l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addTx.o1" "Spline__instance_1:blueprint_spline_4_joint.tx"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint.s" "Spline__instance_1:blueprint_spline_5_joint.is"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_addTx.o1" "Spline__instance_1:blueprint_spline_5_joint.tx"
		 -l on;
connectAttr "Spline__instance_1:creationPose_spline_1_joint.s" "Spline__instance_1:creationPose_spline_2_joint.is"
		 -l on;
connectAttr "Spline__instance_1:creationPose_spline_2_joint.s" "Spline__instance_1:creationPose_spline_3_joint.is"
		 -l on;
connectAttr "Spline__instance_1:creationPose_spline_3_joint.s" "Spline__instance_1:creationPose_spline_4_joint.is"
		 -l on;
connectAttr "Spline__instance_1:creationPose_spline_4_joint.s" "Spline__instance_1:creationPose_spline_5_joint.is"
		 -l on;
connectAttr "non_blueprint_visibilityMultiply.ox" "non_blueprint_grp.v" -l on;
connectAttr "pCube1_skinClusterGroupId.id" "pCubeShape1.iog.og[0].gid" -l on;
connectAttr "pCube1_skinClusterSet.mwc" "pCubeShape1.iog.og[0].gco" -l on;
connectAttr "groupId2.id" "pCubeShape1.iog.og[1].gid" -l on;
connectAttr "tweakSet1.mwc" "pCubeShape1.iog.og[1].gco" -l on;
connectAttr "pCube1_skinCluster.og[0]" "pCubeShape1.i" -l on;
connectAttr "tweak1.vl[0].vt[0]" "pCubeShape1.twl" -l on;
connectAttr "character_grp.animationControlVisibility" "character_container.boc[0]"
		 -l on;
connectAttr "Spline__instance_1:module_container.boc[0]" "character_container.boc[1]"
		 -l on;
connectAttr "Spline__instance_1:module_container.boc[1]" "character_container.boc[2]"
		 -l on;
connectAttr "non_blueprint_container.boc[0]" "character_container.boc[3]" -l on;
connectAttr "hyperLayout3.msg" "character_container.hl" -l on;
connectAttr "Spline__instance_1:SETTINGS.activeModule" "Spline__instance_1:module_container.boc[0]"
		;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:module_container.boc[1]"
		;
connectAttr "hyperLayout2.msg" "Spline__instance_1:module_container.hl" -l on;
connectAttr "non_blueprint_grp.display" "non_blueprint_container.boc[0]";
connectAttr "hyperLayout4.msg" "non_blueprint_container.hl" -l on;
connectAttr "reverse_moduleMaintenanceVisibility.ox" "moduleVisibilityMultiply.i1x"
		 -l on;
connectAttr "character_grp.animationControlVisibility" "moduleVisibilityMultiply.i2x"
		 -l on;
connectAttr "Spline__instance_1:module_container.msg" "hyperLayout3.hyp[0].dn";
connectAttr "character_grp.msg" "hyperLayout3.hyp[1].dn";
connectAttr "reverse_moduleMaintenanceVisibility.msg" "hyperLayout3.hyp[2].dn";
connectAttr "moduleVisibilityMultiply.msg" "hyperLayout3.hyp[3].dn";
connectAttr "non_blueprint_container.msg" "hyperLayout3.hyp[4].dn";
connectAttr "character_grp.moduleMaintenanceVisibility" "reverse_moduleMaintenanceVisibility.ix"
		 -l on;
connectAttr "hyperLayout1.msg" "Spline__instance_1:blueprint_container.hl" -l on
		;
connectAttr "Spline__instance_1:module_grp.msg" "hyperLayout2.hyp[0].dn";
connectAttr "Spline__instance_1:HOOK_IN.msg" "hyperLayout2.hyp[1].dn";
connectAttr "Spline__instance_1:SETTINGS.msg" "hyperLayout2.hyp[2].dn";
connectAttr "Spline__instance_1:blueprint_container.msg" "hyperLayout2.hyp[3].dn"
		;
connectAttr "Spline__instance_1:SETTINGSShape.msg" "hyperLayout2.hyp[4].dn";
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_2_joint_original_Tx.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_5_joint_original_Tx.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Scale.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Scale.i2y"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Scale.i2z"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_3_joint_original_Tx.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_4_joint_original_Tx.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Translate.i2x"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Translate.i2y"
		 -l on;
connectAttr "Spline__instance_1:SETTINGS.creationPoseWeight" "Spline__instance_1:blueprint_spline_1_joint_original_Translate.i2z"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Translate.o" "Spline__instance_1:blueprint_spline_1_joint_addTranslate.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addRotations.o3" "unitConversion1.i"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_dummyRotationsMultiply.o" "Spline__instance_1:blueprint_spline_1_joint_addRotations.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Scale.o" "Spline__instance_1:blueprint_spline_1_joint_addScale.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_dummyRotationsMultiply.o" "Spline__instance_1:blueprint_spline_2_joint_addRotations.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addRotations.o3" "unitConversion2.i"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_original_Tx.ox" "Spline__instance_1:blueprint_spline_2_joint_addTx.i1[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_dummyRotationsMultiply.o" "Spline__instance_1:blueprint_spline_3_joint_addRotations.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addRotations.o3" "unitConversion3.i"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_original_Tx.ox" "Spline__instance_1:blueprint_spline_3_joint_addTx.i1[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_dummyRotationsMultiply.o" "Spline__instance_1:blueprint_spline_4_joint_addRotations.i3[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addRotations.o3" "unitConversion4.i"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_original_Tx.ox" "Spline__instance_1:blueprint_spline_4_joint_addTx.i1[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_original_Tx.ox" "Spline__instance_1:blueprint_spline_5_joint_addTx.i1[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addRotations.msg" "hyperLayout1.hyp[0].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[1].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addTranslate.msg" "hyperLayout1.hyp[2].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Translate.msg" "hyperLayout1.hyp[3].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addScale.msg" "hyperLayout1.hyp[4].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Scale.msg" "hyperLayout1.hyp[5].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addRotations.msg" "hyperLayout1.hyp[6].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[7].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addTx.msg" "hyperLayout1.hyp[8].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_original_Tx.msg" "hyperLayout1.hyp[9].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addRotations.msg" "hyperLayout1.hyp[10].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[11].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addTx.msg" "hyperLayout1.hyp[12].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_original_Tx.msg" "hyperLayout1.hyp[13].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addRotations.msg" "hyperLayout1.hyp[14].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_dummyRotationsMultiply.msg" "hyperLayout1.hyp[15].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addTx.msg" "hyperLayout1.hyp[16].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_original_Tx.msg" "hyperLayout1.hyp[17].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_addTx.msg" "hyperLayout1.hyp[18].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_original_Tx.msg" "hyperLayout1.hyp[19].dn"
		;
connectAttr "Spline__instance_1:blueprint_joints_grp.msg" "hyperLayout1.hyp[20].dn"
		;
connectAttr "Spline__instance_1:creationPose_joints_grp.msg" "hyperLayout1.hyp[21].dn"
		;
connectAttr "unitConversion1.msg" "hyperLayout1.hyp[22].dn";
connectAttr "unitConversion2.msg" "hyperLayout1.hyp[23].dn";
connectAttr "unitConversion3.msg" "hyperLayout1.hyp[24].dn";
connectAttr "unitConversion4.msg" "hyperLayout1.hyp[25].dn";
connectAttr "Spline__instance_1:blueprint_spline_1_joint.msg" "hyperLayout1.hyp[26].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_2_joint.msg" "hyperLayout1.hyp[27].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_3_joint.msg" "hyperLayout1.hyp[28].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_4_joint.msg" "hyperLayout1.hyp[29].dn"
		;
connectAttr "Spline__instance_1:blueprint_spline_5_joint.msg" "hyperLayout1.hyp[30].dn"
		;
connectAttr "Spline__instance_1:creationPose_spline_1_joint.msg" "hyperLayout1.hyp[31].dn"
		;
connectAttr "Spline__instance_1:creationPose_spline_2_joint.msg" "hyperLayout1.hyp[32].dn"
		;
connectAttr "Spline__instance_1:creationPose_spline_3_joint.msg" "hyperLayout1.hyp[33].dn"
		;
connectAttr "Spline__instance_1:creationPose_spline_4_joint.msg" "hyperLayout1.hyp[34].dn"
		;
connectAttr "Spline__instance_1:creationPose_spline_5_joint.msg" "hyperLayout1.hyp[35].dn"
		;
connectAttr "pCube1_skinClusterGroupId.msg" "pCube1_skinClusterSet.gn" -l on -na
		;
connectAttr "pCubeShape1.iog.og[0]" "pCube1_skinClusterSet.dsm" -l on -na;
connectAttr "pCube1_skinCluster.msg" "pCube1_skinClusterSet.ub[0]" -l on;
connectAttr "pCube1_skinClusterGroupParts.og" "pCube1_skinCluster.ip[0].ig" -l on
		;
connectAttr "pCube1_skinClusterGroupId.id" "pCube1_skinCluster.ip[0].gi" -l on;
connectAttr "bindPose1.msg" "pCube1_skinCluster.bp" -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint.wm" "pCube1_skinCluster.ma[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint.wm" "pCube1_skinCluster.ma[1]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint.wm" "pCube1_skinCluster.ma[2]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint.wm" "pCube1_skinCluster.ma[3]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_5_joint.wm" "pCube1_skinCluster.ma[4]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint.liw" "pCube1_skinCluster.lw[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint.liw" "pCube1_skinCluster.lw[1]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint.liw" "pCube1_skinCluster.lw[2]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint.liw" "pCube1_skinCluster.lw[3]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_5_joint.liw" "pCube1_skinCluster.lw[4]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_1_joint.obcc" "pCube1_skinCluster.ifcl[0]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_2_joint.obcc" "pCube1_skinCluster.ifcl[1]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_3_joint.obcc" "pCube1_skinCluster.ifcl[2]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_4_joint.obcc" "pCube1_skinCluster.ifcl[3]"
		 -l on;
connectAttr "Spline__instance_1:blueprint_spline_5_joint.obcc" "pCube1_skinCluster.ifcl[4]"
		 -l on;
connectAttr "groupId2.msg" "tweakSet1.gn" -l on -na;
connectAttr "pCubeShape1.iog.og[1]" "tweakSet1.dsm" -l on -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]" -l on;
connectAttr "reverse_moduleMaintenanceVisibility.ox" "non_blueprint_visibilityMultiply.i1x"
		 -l on;
connectAttr "non_blueprint_grp.display" "non_blueprint_visibilityMultiply.i2x" -l
		 on;
connectAttr "groupParts2.og" "tweak1.ip[0].ig" -l on;
connectAttr "groupId2.id" "tweak1.ip[0].gi" -l on;
connectAttr "tweak1.og[0]" "pCube1_skinClusterGroupParts.ig" -l on;
connectAttr "pCube1_skinClusterGroupId.id" "pCube1_skinClusterGroupParts.gi" -l on
		;
connectAttr "pCubeShape1Orig.w" "groupParts2.ig" -l on;
connectAttr "groupId2.id" "groupParts2.gi" -l on;
connectAttr "non_blueprint_grp.msg" "hyperLayout4.hyp[0].dn";
connectAttr "pCube1.msg" "hyperLayout4.hyp[1].dn";
connectAttr "pCubeShape1.msg" "hyperLayout4.hyp[2].dn";
connectAttr "pCubeShape1Orig.msg" "hyperLayout4.hyp[3].dn";
connectAttr "pCube1_skinClusterSet.msg" "hyperLayout4.hyp[4].dn";
connectAttr "pCube1_skinCluster.msg" "hyperLayout4.hyp[5].dn";
connectAttr "tweakSet1.msg" "hyperLayout4.hyp[6].dn";
connectAttr "non_blueprint_visibilityMultiply.msg" "hyperLayout4.hyp[7].dn";
connectAttr "tweak1.msg" "hyperLayout4.hyp[8].dn";
connectAttr "pCube1_skinClusterGroupId.msg" "hyperLayout4.hyp[9].dn";
connectAttr "pCube1_skinClusterGroupParts.msg" "hyperLayout4.hyp[10].dn";
connectAttr "groupId2.msg" "hyperLayout4.hyp[11].dn";
connectAttr "groupParts2.msg" "hyperLayout4.hyp[12].dn";
connectAttr "Spline__instance_1:module_grp.msg" "bindPose1.m[0]";
connectAttr "Spline__instance_1:HOOK_IN.msg" "bindPose1.m[1]";
connectAttr "Spline__instance_1:blueprint_joints_grp.msg" "bindPose1.m[2]";
connectAttr "Spline__instance_1:blueprint_spline_1_joint.msg" "bindPose1.m[3]";
connectAttr "Spline__instance_1:blueprint_spline_2_joint.msg" "bindPose1.m[4]";
connectAttr "Spline__instance_1:blueprint_spline_3_joint.msg" "bindPose1.m[5]";
connectAttr "Spline__instance_1:blueprint_spline_4_joint.msg" "bindPose1.m[6]";
connectAttr "Spline__instance_1:blueprint_spline_5_joint.msg" "bindPose1.m[7]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "bindPose1.m[2]" "bindPose1.p[3]";
connectAttr "bindPose1.m[3]" "bindPose1.p[4]";
connectAttr "bindPose1.m[4]" "bindPose1.p[5]";
connectAttr "bindPose1.m[5]" "bindPose1.p[6]";
connectAttr "bindPose1.m[6]" "bindPose1.p[7]";
connectAttr "Spline__instance_1:blueprint_spline_1_joint.bps" "bindPose1.wm[3]";
connectAttr "Spline__instance_1:blueprint_spline_2_joint.bps" "bindPose1.wm[4]";
connectAttr "Spline__instance_1:blueprint_spline_3_joint.bps" "bindPose1.wm[5]";
connectAttr "Spline__instance_1:blueprint_spline_4_joint.bps" "bindPose1.wm[6]";
connectAttr "Spline__instance_1:blueprint_spline_5_joint.bps" "bindPose1.wm[7]";
connectAttr "pCubeShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addTranslate.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Translate.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_addScale.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_1_joint_original_Scale.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_2_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_3_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addRotations.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_dummyRotationsMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_4_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_addTx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "Spline__instance_1:blueprint_spline_5_joint_original_Tx.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "reverse_moduleMaintenanceVisibility.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "moduleVisibilityMultiply.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "non_blueprint_visibilityMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
// End of cube_spline.ma
