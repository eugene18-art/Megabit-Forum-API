<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use App\Models\User;

class CreateUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->char('username', 150)->unique()->nullable();
            $table->char('email', 254)->unique();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');
            $table->rememberToken();

            $table->char('first_name', 30);
            $table->char('last_name', 150);
            $table->enum('types', User::$MEMBER_TYPES)->default(User::$MEMBER_TYPES['regular']);
            $table->date('birth_date');
            $table->char('birth_place', 255);
            $table->enum('gender', User::$GENDER_TYPES);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('users');
    }
}
