<?php

namespace App\Traits;

use App\Exceptions\ApiException;
use App\Models\User;

trait Permissions {
    public function isOwner($request, $obj) {
        if ($request->user()->id == $obj) {
            return true;
        }
        throw new ApiException('You must be the owner to do this.', 401);
    }

    public function isAdminOrOwner($request, $obj) {
        if (($request->user()->id == $obj) || ($request->user()->types == User::$MEMBER_TYPES['admin'])) {
            return true;
        }
        throw new ApiException("You must be owner or admin to do this", 401);
    }
}

