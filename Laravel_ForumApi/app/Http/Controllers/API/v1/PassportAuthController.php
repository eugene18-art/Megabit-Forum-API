<?php

namespace App\Http\Controllers\API\v1;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use App\Models\User;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Auth;

class PassportAuthController extends Controller
{
    /**
     * User Signup handler
     */
    private static $rfc5322 = "/(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/";
    public function signup(Request $request) {
        
        $validator = Validator::make($request->all(), [
            'first_name'=>'required|max:30',
            'last_name'=>'required|max:150',
            'username'=>'required|unique:users|max:150',
            'email'=>['required', 'unique:users', 'max:254', "regex:{$this::$rfc5322}"],
            'password'=>'required|same:confirm_password',
            'confirm_password'=>'required|same:password',
            'types'=>['required', Rule::in(User::$MEMBER_TYPES)],
            'birth_date'=>'required|date_format:Y-m-d\TH:i:s\Z',
            'birth_place'=>'required',
            'gender'=>['required', Rule::in(User::$GENDER_TYPES)],
        ]);

        if ($validator->fails()) {
            return response()->json($validator->errors(), 400);
        }

        $validated_data = $validator->valid();
        $validated_data['birth_date'] = Carbon::parse($validated_data['birth_date']);
        $validated_data['password'] = bcrypt($validated_data['password']);

        $user = User::create($validated_data);
        $token = $user->createToken('MegabitForumApiToken')->accessToken;
        Auth::login($user);

        $response_data = $user->toArray()+[
            'token'=>$token,
        ];
        return response()->json($response_data, 201);
    }

    public function signin(Request $request) {
        $validator = Validator::make($request->all(), [
            'email'=>'required|email',
            'password'=>'required'
        ]);

        $validated_data = $validator->valid();
        if (Auth::attempt($validated_data)) {
            $user = Auth::user();
            $token = $user->createToken('MegabitForumApiToken')->accessToken;
            $response_data = $user->toArray()+[
                'token'=>$token,
            ];
            Auth::login($user);
            return response()->json($response_data, 200);
        } else {
            return response()->json(['detail'=>'Login failed! Check your login credentials.'], 400);
        }
    }

    public function signout() {
        Auth::user()->tokens->each(function($token) {
            $token->delete();
        });
        return response()->json(['detail'=>'Logout success!'], 200);
    }
}
