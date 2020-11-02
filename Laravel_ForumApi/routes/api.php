<?php

use App\Http\Controllers\API\v1\PassportAuthController;
use App\Http\Controllers\API\v1\PostController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
Route::prefix('v1')->group(function() {
    Route::prefix('auth')->group(function() {
        Route::post('signup/', [PassportAuthController::class, 'signup'])->name('signup');
        Route::post('signin/', [PassportAuthController::class, 'signin'])->name('signin');
        Route::middleware('auth:api')->get('signout/', [PassportAuthController::class, 'signout'])->name('signout');
    });
    Route::middleware('auth:api')->resource('posts', PostController::class);
});


// Route::middleware('auth:api')->get('/user', function (Request $request) {
//     return $request->user();
// });
