// 1. Any user can see public images.
permit (
    principal,
    action == Action::"view",
    resource
) when {
    resource.isPublic
};

// 2. Any user can view and delete their own images

// 3. Admins can delete public images of any user

// 4. Users under the age of 18 (or guests) should not see images marked explicit
